using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace IDCard.Helper
{
    public class APIHelper
    {
          private static readonly string url = App.ApiURL + "/";
          private static readonly string restfull = url + "api/";
          // GET
          public static T SendGetRequest<T>(string path)
          {
               T data = default(T);
               using (var client = new HttpClient())
               {
                    var req = client.GetAsync(restfull + path);
                    HttpResponseMessage res = req.Result;
                    var result = res.Content.ReadAsStringAsync().Result;
                    if (res.IsSuccessStatusCode)
                    {
                         data = JsonConvert.DeserializeObject<T>(result);
                    }
               }
               return data;
          }
          // POST
          public static bool SendPostRequest<T>(string path, T p)
          {
               bool objectOut = false;
               using (var client = new HttpClient())
               {
                    var data = JsonConvert.SerializeObject(p);
                    var httpContent = new StringContent(data, Encoding.UTF8, "application/json");
                    client.BaseAddress = new Uri(restfull);
                    var res = client.PostAsync(path, httpContent).Result;
                    if (res.IsSuccessStatusCode)
                    {
                         var result = res.Content.ReadAsStringAsync().Result;
                         //objectOut = JsonConvert.DeserializeObject<bool>(result);
                    }
               }
               return objectOut;
          }

     }
}
