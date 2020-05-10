using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;
using System.Net.Http;
using Android.Graphics;
using System.IO;
using IDCard;
using System.Text.RegularExpressions;

namespace IDCard
{
     public partial class MainPage : ContentPage
     {
          public MainPage()
          {
               InitializeComponent();
          }
          byte[] imageBytes;
          private static readonly HttpClient client = new HttpClient();
          private async void BtnCamera_Clicked(object sender, EventArgs e)
          {
               var photo = await Plugin.Media.CrossMedia.Current.TakePhotoAsync(new Plugin.Media.Abstractions.StoreCameraMediaOptions() { });

               if (photo != null)
               {
                    var stream = photo.GetStream();
                    imgPhoto.Source = ImageSource.FromStream(() => { return stream; });
                    using (var memoryStreamHandler = new MemoryStream())
                    {
                         photo.GetStream().CopyTo(memoryStreamHandler);
                         imageBytes = memoryStreamHandler.ToArray();
                    }
               }
          }
          //https://stackoverflow.com/questions/46614727/xamarin-forms-convert-imagesource-to-actual-png-image-and-store-on-device?rq=1
          private void BtnSave_Clicked(object sender, EventArgs e)
          {
               //string path =  Android.OS.Environment.GetExternalStoragePublicDirectory(Android.OS.Environment.DirectoryDownloads).AbsolutePath;
               //File.WriteAllBytes(path + "/hey.png", imageBytes);
               Helper.APIHelper.SendPostRequest<byte[]>("app",imageBytes);
          }

          private void BtnSetServer_Clicked(object sender, EventArgs e)
          {
               if (IsValidateIP(entIP.Text))
               {
                    if (IsValidatePort(entPort.Text))
                    {
                         App.ApiURL = String.Format("http://{0}:{1}", entIP.Text, entPort.Text);
                    }
                    else
                    {
                         entPort.PlaceholderColor = Xamarin.Forms.Color.Red;
                    }
               }                    
               else
               {
                    entIP.PlaceholderColor = Xamarin.Forms.Color.Red;
               }
          }
          private void BtnExtract_Clicked(object sender, EventArgs e)
          {
               string path = Android.OS.Environment.GetExternalStoragePublicDirectory(Android.OS.Environment.DirectoryDownloads).AbsolutePath;
               var x = File.ReadAllBytes(path + "/hey.png");
               imgPhoto.Source = ImageSource.FromStream(() => { return new MemoryStream(x); });
          }
          public bool IsValidateIP(string Address)
          {
               //Match pattern for IP address    
               string Pattern = @"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$";
               //Regular Expression object    
               Regex check = new Regex(Pattern);

               //check to make sure an ip address was provided    
               if (string.IsNullOrEmpty(Address))
                    //returns false if IP is not provided    
                    return false;
               else
                    //Matching the pattern    
                    return check.IsMatch(Address, 0);
          }
          public bool IsValidatePort(string Port)
          {
               //check to make sure an ip address was provided    
               if (string.IsNullOrEmpty(Port))
                    //returns false if IP is not provided    
                    return false;
               var check = int.TryParse(Port, out int x);
               if (check)
                    if (x <= 0)
                         check = false;
               return check;
          }

          private void EntIP_Focused(object sender, FocusEventArgs e)
          {

          }

          private void EntIP_Unfocused(object sender, FocusEventArgs e)
          {

          }

          private void EntPort_Focused(object sender, FocusEventArgs e)
          {

          }

          private void EntPort_Unfocused(object sender, FocusEventArgs e)
          {

          }
     }
}
