/*
 * @Author: 王琨
 * @Date: 2021-10-21 10:34:58
 * @Descripttion:
 */
var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "113.237.245.227",
        port: 57114
      }
    }
  };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "17610040106",
            password: "081300ykp,"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);