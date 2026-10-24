param(
    [ValidateSet('Install', 'Read')]
    [string]$Mode = 'Install',
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]{0,62}$')]
    [string]$Subdomain
)

$ErrorActionPreference = 'Stop'
$credentialTarget = "Kommo:$Subdomain.kommo.com"

$nativeCode = @'
using System;
using System.Runtime.InteropServices;

public static class KommoCredentialNative
{
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct NativeCredential
    {
        public UInt32 Flags;
        public UInt32 Type;
        public IntPtr TargetName;
        public IntPtr Comment;
        public Int64 LastWritten;
        public UInt32 CredentialBlobSize;
        public IntPtr CredentialBlob;
        public UInt32 Persist;
        public UInt32 AttributeCount;
        public IntPtr Attributes;
        public IntPtr TargetAlias;
        public IntPtr UserName;
    }

    [DllImport("advapi32.dll", EntryPoint = "CredWriteW", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CredWrite(ref NativeCredential credential, UInt32 flags);

    [DllImport("advapi32.dll", EntryPoint = "CredReadW", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CredRead(string target, UInt32 type, UInt32 flags, out IntPtr credential);

    [DllImport("advapi32.dll", EntryPoint = "CredFree", SetLastError = false)]
    private static extern void CredFree(IntPtr credential);

    public static bool WriteCredential(string target, byte[] blob)
    {
        if (blob == null || blob.Length == 0 || blob.Length > 5120) return false;

        GCHandle pinnedBlob = GCHandle.Alloc(blob, GCHandleType.Pinned);
        IntPtr targetName = IntPtr.Zero;
        IntPtr userName = IntPtr.Zero;
        try
        {
            targetName = Marshal.StringToCoTaskMemUni(target);
            userName = Marshal.StringToCoTaskMemUni("KOMMO_LONG_LIVED_TOKEN");

            NativeCredential credential = new NativeCredential();
            credential.Type = 1; // CRED_TYPE_GENERIC
            credential.TargetName = targetName;
            credential.CredentialBlobSize = (UInt32)blob.Length;
            credential.CredentialBlob = pinnedBlob.AddrOfPinnedObject();
            credential.Persist = 2; // CRED_PERSIST_LOCAL_MACHINE
            credential.UserName = userName;
            return CredWrite(ref credential, 0);
        }
        finally
        {
            if (userName != IntPtr.Zero) Marshal.FreeCoTaskMem(userName);
            if (targetName != IntPtr.Zero) Marshal.FreeCoTaskMem(targetName);
            if (pinnedBlob.IsAllocated) pinnedBlob.Free();
        }
    }

    public static bool TryReadCredential(string target, out byte[] blob)
    {
        blob = null;
        IntPtr credentialPointer;
        if (!CredRead(target, 1, 0, out credentialPointer)) return false;

        try
        {
            NativeCredential credential = (NativeCredential)Marshal.PtrToStructure(
                credentialPointer, typeof(NativeCredential));
            if (credential.CredentialBlobSize == 0 || credential.CredentialBlobSize > 5120) return false;

            blob = new byte[credential.CredentialBlobSize];
            Marshal.Copy(credential.CredentialBlob, blob, 0, blob.Length);
            return true;
        }
        finally
        {
            CredFree(credentialPointer);
        }
    }
}
'@

function Test-TokenBytes {
    param([Parameter(Mandatory)][byte[]]$Bytes)

    if ($Bytes.Length -lt 64 -or $Bytes.Length -gt 5120) { return $false }
    $dotCount = 0
    $segmentLength = 0
    foreach ($value in $Bytes) {
        if ($value -eq 46) {
            if ($segmentLength -eq 0) { return $false }
            $dotCount++
            $segmentLength = 0
            continue
        }

        $isAllowed = (($value -ge 48 -and $value -le 57) -or
            ($value -ge 65 -and $value -le 90) -or
            ($value -ge 97 -and $value -le 122) -or
            $value -eq 45 -or $value -eq 95)
        if (-not $isAllowed) { return $false }
        $segmentLength++
    }
    return ($dotCount -eq 2 -and $segmentLength -gt 0)
}

try {
    Add-Type -TypeDefinition $nativeCode -ErrorAction Stop

    if ($Mode -eq 'Read') {
        [byte[]]$storedBytes = $null
        if (-not [KommoCredentialNative]::TryReadCredential($credentialTarget, [ref]$storedBytes) -or
            -not (Test-TokenBytes -Bytes $storedBytes)) {
            throw 'Credencial indisponível.'
        }
        try {
            [Console]::Out.Write([System.Text.UTF8Encoding]::new($false, $true).GetString($storedBytes))
            [Console]::Out.Flush()
        }
        finally {
            [Array]::Clear($storedBytes, 0, $storedBytes.Length)
        }
        exit 0
    }

    Write-Host "Kommo: instalar token localmente para $Subdomain.kommo.com" -ForegroundColor Cyan
    $secureToken = Read-Host 'Cole o token de longa duração (a entrada ficará mascarada)' -AsSecureString
    if ($null -eq $secureToken -or $secureToken.Length -eq 0) { throw 'Token vazio.' }

    $bstr = [IntPtr]::Zero
    [char[]]$characters = $null
    [byte[]]$tokenBytes = $null
    [byte[]]$readBack = $null
    try {
        $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
        $characterCount = [Runtime.InteropServices.Marshal]::ReadInt32($bstr, -4) / 2
        $characters = [char[]]::new($characterCount)
        [Runtime.InteropServices.Marshal]::Copy($bstr, $characters, 0, $characterCount)
        $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
        $tokenBytes = $utf8.GetBytes($characters)

        if (-not (Test-TokenBytes -Bytes $tokenBytes)) { throw 'Formato inválido.' }
        if (-not [KommoCredentialNative]::WriteCredential($credentialTarget, $tokenBytes)) {
            throw 'Gravação recusada.'
        }

        if (-not [KommoCredentialNative]::TryReadCredential($credentialTarget, [ref]$readBack)) {
            throw 'Leitura de confirmação falhou.'
        }
        $matches = $readBack.Length -eq $tokenBytes.Length
        $difference = 0
        if ($matches) {
            for ($index = 0; $index -lt $tokenBytes.Length; $index++) {
                $difference = $difference -bor ($tokenBytes[$index] -bxor $readBack[$index])
            }
        }
        if (-not $matches -or $difference -ne 0) { throw 'Confirmação da gravação falhou.' }

        Write-Host "Token salvo e confirmado no Gerenciador de Credenciais do Windows para $Subdomain.kommo.com." -ForegroundColor Green
        Write-Host 'Reinicie o cliente MCP para carregar a credencial.' -ForegroundColor Cyan
    }
    finally {
        if ($bstr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
        if ($null -ne $characters) { [Array]::Clear($characters, 0, $characters.Length) }
        if ($null -ne $tokenBytes) { [Array]::Clear($tokenBytes, 0, $tokenBytes.Length) }
        if ($null -ne $readBack) { [Array]::Clear($readBack, 0, $readBack.Length) }
        if ($null -ne $secureToken) { $secureToken.Dispose() }
    }
}
catch {
    if ($Mode -eq 'Read') {
        [Console]::Error.WriteLine('Kommo: credencial não disponível no cofre do Windows.')
        exit 2
    }
    [Console]::Error.WriteLine('Kommo: não foi possível salvar e confirmar o token. Revise a janela do PowerShell e tente novamente.')
    exit 1
}
