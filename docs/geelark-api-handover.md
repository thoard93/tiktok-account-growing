# GeeLark API Handover Document

> **Source:** https://open.geelark.com/api  
> **Base URL:** `https://openapi.geelark.com`  
> **Protocol:** All requests use `POST`. Request body must be `JSON`. Set `Content-Type: application/json`.
> **Rate Limit:** 200 requests/minute · 24,000 requests/hour. Exceeding the limit restricts the API for 2 hours (auto-unblocked after 2 hours).
> **Auth:** Two methods — API Key verification and Token verification (see Authentication section).

---

## Table of Contents

- **General**
  - [General](#general)
- **User Guide**
    - [User Guide / Cloud Phone](#user-guide--cloud-phone)
    - [User Guide / Browser](#user-guide--browser)
- **Cloud Phone API**
    - [Cloud Phone API / Cloud Phone Management](#cloud-phone-api--cloud-phone-management)
      - [Cloud Phone API / Automation / Task Management](#cloud-phone-api--automation--task-management)
      - [Cloud Phone API / Automation / TikTok](#cloud-phone-api--automation--tiktok)
      - [Cloud Phone API / Automation / Facebook](#cloud-phone-api--automation--facebook)
      - [Cloud Phone API / Automation / Instagram](#cloud-phone-api--automation--instagram)
      - [Cloud Phone API / Automation / YouTube](#cloud-phone-api--automation--youtube)
      - [Cloud Phone API / Automation / Google](#cloud-phone-api--automation--google)
      - [Cloud Phone API / Automation / Shein](#cloud-phone-api--automation--shein)
      - [Cloud Phone API / Automation / X(Twitter)](#cloud-phone-api--automation--xtwitter)
      - [Cloud Phone API / Automation / Reddit](#cloud-phone-api--automation--reddit)
      - [Cloud Phone API / Automation / Pinterest](#cloud-phone-api--automation--pinterest)
      - [Cloud Phone API / Automation / Threads](#cloud-phone-api--automation--threads)
      - [Cloud Phone API / Automation / Custom Task](#cloud-phone-api--automation--custom-task)
      - [Cloud Phone API / Automation / Other Task](#cloud-phone-api--automation--other-task)
    - [Cloud Phone API / Shell](#cloud-phone-api--shell)
    - [Cloud Phone API / Application Management](#cloud-phone-api--application-management)
    - [Cloud Phone API / ADB](#cloud-phone-api--adb)
    - [Cloud Phone API / File Management](#cloud-phone-api--file-management)
    - [Cloud Phone API / Library](#cloud-phone-api--library)
    - [Cloud Phone API / Webhook](#cloud-phone-api--webhook)
    - [Cloud Phone API / OEM/White Label](#cloud-phone-api--oemwhite-label)
    - [Cloud Phone API / Analytics](#cloud-phone-api--analytics)
- **Browser API**
    - [Browser API / Browser Management](#browser-api--browser-management)
      - [Browser API / Automation / Task Management](#browser-api--automation--task-management)
      - [Browser API / Automation / TikTok](#browser-api--automation--tiktok)
      - [Browser API / Automation / Facebook](#browser-api--automation--facebook)
      - [Browser API / Automation / Instagram](#browser-api--automation--instagram)
      - [Browser API / Automation / YouTube](#browser-api--automation--youtube)
      - [Browser API / Automation / X(Twitter)](#browser-api--automation--xtwitter)
      - [Browser API / Automation / Reddit](#browser-api--automation--reddit)
      - [Browser API / Automation / Custom Task](#browser-api--automation--custom-task)
      - [Browser API / Automation / Other Task](#browser-api--automation--other-task)
- **Proxy Management**
  - [Proxy Management](#proxy-management)
- **Tag Management**
  - [Tag Management](#tag-management)
- **Group Management**
  - [Group Management](#group-management)
- **Billing**
  - [Billing](#billing)
- **Error Codes**
  - [Error Codes](#error-codes)
- **API Document Download**
  - [API Document Download](#api-document-download)

---

## General

### Change log

[TOC]
### 2026.04.22
#### Cloud Phone
- Instagram posts Reels videos and supports sharing links.
- Instagram posts Reels photo albums and supports sharing links.
- TikTok AI-generated random comments support keyword search.
- Added interface for retrieving cloud phone network settings
- Added interface for modifying cloud phone network settings
- OEM API supports custom configuration of the iconUrl

#### Browser
- Added interface for cloning browser
- Launch browser API supports WebHook callback.

### 2026.04.13
#### Cloud Phone
- Added a clone cloud phone API

### 2026.04.08
#### Cloud Phone
- Creating and modifying cloud phone information supports setting proxy detection channels.
- Google's auto-sign-in task supports 2fa
- Added API for posting tasks to hide all TikTok videos
- Added API for posting tasks to hide all TikTok videos (Asia)
- Added API for posting tasks to delete all TikTok videos
- Added API for posting tasks to delete all TikTok videos (Asia)

#### Browser
- Browser API interfaces require token verification.
- Added API for Facebook posting tasks
- Added API for Twitter retweeting and posting tasks
- Added API for Cookie bot tasks
- Added API for YouTube video viewing tasks
- Added API for browsing and liking Instagram profile tasks
- Added API for TikTok video search, liking, and commenting tasks
- Added API for Instagram topic search and post browsing tasks
- Added API for browsing and liking Reddit keyword search posts tasks
- Added API for TikTok video likes and comments
- Added API for Facebook friend recommendation tasks
- Added API for TikTok video likes
- Added API for liking all Facebook profiles
- Added API for Twitter tweet likes and retweets
- Added API for Facebook profile creation tasks

#### Proxy Management
- Creating and modifying proxy supports setting proxy detection channels.

### 2026.04.07
#### Billing
- Added billing transaction detail interface

### 2026.04.03
#### Cloud Phone
- TikTok releases photo gallery task to support product settings

### 2026.03.30
#### Browser
- Create and update interfaces now support setting time zone, language, and resolution
- List interface now returns time zone, language, and resolution settings

#### Cloud Phone
- Added Import/Export custom task flow interfaces

### 2026.03.25
#### Cloud Phone
- Added Instagram edit profile task interface
- Added page parameter to Facebook Reels video publishing interface

#### Browser
- Added "resume last visit" parameter to browser creation and update interfaces
- Added "open specified URL" parameter to browser creation and update interfaces

### 2026.03.18
#### Cloud Phone
- Added US region for Android 15; set region parameter to 'us' when creating a new cloud phone via Create Cloud Phone / Create Cloud Phone V2

#### Browser
- Browser now supports 2FA secret keys
- Added set browser bookmarks interface
- Added get browser bookmarks interface

### 2026.03.11
#### Cloud Phone
- TikTok random like and TikTok AI random comment now support probability parameter
- Added create TikTok random follow task interface

#### Browser
- Added get browser task detail interface
- Added check browser status interface
- Added clear browser cache interface
- Added move browser group interface
- Added get environment cookies interface

### 2026.02.27
#### Other
- Added response parameter `availableMonthlyRentals` to get current subscription info interface

### 2026.02.25
#### Cloud Phone
- Added `fileName` parameter to add asset interface
- Added `ids` parameter to get assets interface

#### Other
- Added get current subscription info interface

### 2026.02.10
#### Cloud Phone
- Added post parameter to Instagram Reels album publishing interface

### 2026.02.06
#### Other
- Added get subscription list and change subscription interfaces

### 2026.02.04
#### Cloud Phone
- Android 14 now supports app keep-alive
- TikTok AI random comment now supports specified links

#### Browser
- Added browser task interface

### 2026.01.27
#### Cloud Phone
- Added request parameter `proxyIds` to get cloud phone list interface

### 2026.01.26
#### Cloud Phone
- Added response parameters `deviceName`, `netType`, `language`, `province`, `city` to get cloud phone list interface

### 2026.01.23
#### Cloud Phone
- Added parameter `energySavingMode` to start cloud phone interface

### 2026.01.21
#### Cloud Phone
- Added device name parameter to create cloud phone interface
- Instagram Reels video and album publishing interfaces now support AI tags
- Added set team app keep-alive and set team app auto-start interfaces
- Added app installation callback

### 2026.01.20
#### Cloud Phone
- Added batch import contacts to cloud phone interface

### 2026.01.19
#### Cloud Phone
- Added cloud phone [error code](https://open.geelark.cn/api/cloud-phone-error-codes) summary

### 2026.01.14
#### Cloud Phone
- Added move cloud phone group interface

### 2026.01.12
#### Cloud Phone
- Added `toolBarSettings` parameter to OEM custom settings

### 2026.01.08
#### Cloud Phone
- One-click new device interface now supports retaining phone number, region, language, and network type

### 2026.01.07
#### Cloud Phone
- Instagram Reels video publishing interface now supports "use same audio" URL and volume parameters
- Instagram Reels album publishing interface now supports "use same audio" URL parameter
- Added app hide accessibility service interface

### 2026.01.04
#### Cloud Phone
- Update cloud phone info interface now supports custom phone number
- Create cloud phone now supports custom language

### 2025.12.29
#### Cloud Phone
- Added `mirrorUrl` parameter to cloud phone custom settings

### 2025.12.25
#### Cloud Phone
- Create cloud phone now supports setting region

### 2025.12.24
#### Cloud Phone
- Power on/off callbacks now return username, IP, and event time
- Added `hideMirror` parameter to start cloud phone interface
- Start cloud phone interface now returns billing type
- Added device maintenance error codes to start cloud phone and create cloud phone V2 interfaces
- Added task creation and task completion callbacks
- Added update data assistant account interface

### 2025.12.19
#### Cloud Phone
- Added environment tag change callback
- Added batch app operations interface

### 2025.12.18
#### Cloud Phone
- Added environment name change and environment deletion callbacks

### 2025.12.16
#### Cloud Phone
- Added `openStatus` filter parameter to `/open/v1/phone/list`
- Added get team app list interface
- Added remove team app interface
- Added set team app auto-install interface
- Added set team app authorization interface
- Added set team app ROOT interface
- Create cloud phone now supports Proxyma, DECODO, NodeMaven, IPIDEAMobile, and kookeeyMobile proxies
- Batch query tasks interface now supports filtering by task ID
- Added `rpaStatus` to cloud phone list response

### 2025.12.15
#### Cloud Phone
- Added `hideLibrary` parameter to start cloud phone interface

### 2025.12.12
#### Cloud Phone
- Added `center` parameter to start cloud phone interface

### 2025.12.11
#### Cloud Phone
- Added common ADB commands documentation for cloud phone
- Send SMS to cloud phone interface now supports Android 14

### 2025.12.10
#### Browser
- Create and update browser interfaces now support passing startup parameters

### 2025.12.03
#### Cloud Phone
- Added `width` parameter to start cloud phone interface

### 2025.11.28
#### Cloud Phone
- Added data assistant account data retrieval interface

### 2025.11.26
#### Cloud Phone
- Added custom template task publishing failure to task failure reasons

### 2025.11.12
#### Cloud Phone
- Attachments can now be transferred when transferring environments
- Instagram AI account nurturing now supports configurable number of videos to browse and search keywords

### 2025.11.03
#### Other
- Added proxy detection interface

### 2025.10.29
#### Cloud Phone
- Added Threads video publishing task interface
- Added Threads post publishing task interface

### 2025.10.22
#### Cloud Phone
- Added `hideSideBar` and `displayTimer` parameters to start cloud phone interface
- Added shutdown callback for cloud phone
- Added get app list interface
- Added add app to team app interface

### 2025.10.21
#### Cloud Phone
- Added TikTok AI random comment (Asia) task interface
- ADB is now available for cloud phone Android 9

### 2025.10.16
#### Cloud Phone
- Create cloud phone now supports passing phone number
- Reddit account nurturing now supports passing search keywords

#### Browser
- Added browser interface documentation
- Added create browser interface
- Added update browser interface
- Added delete browser interface
- Added get browser interface
- Added start browser interface
- Added close browser interface
- Added transfer browser interface

### 2025.10.15
#### Cloud Phone
- Cloud phone list interface now returns monthly subscription expiration time

### 2025.08.26
#### Cloud Phone
- Cloud phone list now supports filtering by billing mode; added billing mode field to response
- Create TikTok add video/album/nurturing tasks now support adding notes

### 2025.08.20
#### Cloud Phone
- Create cloud phone now supports setting network type
- Added set cloud phone network type interface
- Added Pinterest video publishing interface
- Added Pinterest post publishing interface
- Added update cloud phone logo/brand name interface

### 2025.08.19
#### Cloud Phone
- Keybox upload interface

### 2025.07.24
#### Cloud Phone
- TikTok video and album publishing tasks can now retrieve share links
- Task query interface now returns share link
- Added Instagram auto-login interface

### 2025.07.21
#### Cloud Phone
- Uninstall app now supports uninstalling by package name

### 2025.07.14
#### Cloud Phone
- Added batch query tasks interface

### 2025.07.10
#### Cloud Phone
- TikTok video publishing task now supports setting cover image
- Added batch import contacts to cloud phone interface
- Added upload keybox to cloud phone interface
- Added TikTok random like (Asia) interface
- Added TikTok send direct message (Asia) interface
- Added Instagram Reels album publishing interface

### 2025.07.04
#### Cloud Phone
- YouTube Shorts publishing interface: "use same audio" URL is now optional

### 2025.07.01
#### Cloud Phone
- Proxy query interface now returns proxy sequence number
- Added create cloud phone V2 interface

### 2025.06.26
#### Cloud Phone
- Added Reddit AI account nurturing interface
- Added Reddit video publishing interface
- Added Reddit post publishing interface
- Added Google download app interface
- Added Google open app browse interface
- Added TikTok send direct message interface
- Added Facebook send direct message interface
- Added Instagram send direct message interface
- Added transfer cloud phone interface
- Added asset center related interfaces

### 2025.06.12
#### Cloud Phone
- Added error code for disallowed proxy type to create cloud phone interface
- Added error code for disallowed proxy type to update proxy interface
- Added error code for disallowed proxy type to update cloud phone info interface
- Added get task detail interface
- Added token authentication support

### 2025.05.29
#### Cloud Phone
- TikTok video and album publishing tasks now support marking AI-generated content

### 2025.05.15
#### Cloud Phone
- TikTok add video/album/nurturing task interfaces no longer have time interval restrictions
- Environment group notes now support up to 500 characters
- Create cloud phone interface now returns cloud phone device information

### 2025.04.25
#### Cloud Phone
- Get cloud phone list now supports querying by ID and returns proxy information

### 2025.04.24
#### Cloud Phone
- TikTok video and album publishing now support setting volume
- Added task workflow query interface
- Added create custom task interface
- Added Instagram AI account nurturing interface

### 2025.04.10
#### Cloud Phone
- Added "in use" error code to delete cloud phone interface
- Task query interface now returns duration field

### 2025.04.09
#### Cloud Phone
- For TikTok add video/album/nurturing tasks, if the scheduled time is earlier than the current time, the current time will be used.

### 2025.04.07
#### Cloud Phone
- Modified TikTok account nurturing task parameters

### 2025.04.01
#### Cloud Phone
- Added create X (Twitter) post and batch upload files to cloud phone task interfaces

### 2025.03.25
#### Cloud Phone
- ADB now supports Android 14

### 2025.03.24
#### Cloud Phone
- Added new field `changeBrandModel` to one-click new device V2 interface to control whether to randomize cloud phone brand and model

### 2025.03.20
#### Cloud Phone
- Added automation module, including automation tasks for multiple platforms

### 2025.03.13
#### Cloud Phone
- Added get cloud phone brand list interface
- Create cloud phone interface now supports passing brand and model

### 2025.03.06
#### Cloud Phone
- Running tasks can now be canceled
- When adding tasks, the scheduled time interval for the same cloud phone cannot be less than 10 minutes
- Video and album publishing tasks now support specifying retry count and timeout
- Execute shell and create cloud phone now support Android 14

### 2025.02.28
#### Cloud Phone
- Added album title field to TikTok automation add task for album publishing

### 2025.02.12
#### Other
- Added payment-related interfaces

### 2025.02.10
#### Cloud Phone
- Get cloud phone list now returns device information fields: brand, model

### 2025.02.07
#### Cloud Phone
- Added interface: send SMS to cloud phone

### 2025.01.14
#### Cloud Phone
- Added video publishing task parameter fields to TikTok automation add task interface

### 2024.12.25
#### Cloud Phone
- Launched get cloud phone device ID interface

### 2024.12.19
#### Cloud Phone
- Launched set ROOT status interface

### 2024.11.25
#### Cloud Phone
- Launched screenshot-related interfaces

### 2024.11.21
#### Cloud Phone
- Get cloud phone list now returns cloud phone device information fields

### 2024.10.28
#### Cloud Phone
- Launched download file to cloud phone interface
- Launched one-click new device V2 interface; the original one-click new device interface will no longer rely on callbacks

### 2024.10.09
#### Cloud Phone
- Launched file upload related interfaces
- Added video publishing task parameter fields to TikTok automation add task interface
- Fixed ADB get ADB information retrieval issue

### 2024.09.25
#### Cloud Phone
- Launched one-click new device related interfaces

### 2024.08.28
#### Cloud Phone
- Launched tag related interfaces
- Launched set/get cloud phone GPS interfaces
- Launched group related interfaces

### 2024.08.13
#### Cloud Phone
- Launched app management related interfaces

### 2024.08.09
#### Cloud Phone
- Launched ADB related interfaces

### 2024.06.04
#### Cloud Phone
- API interfaces launched

---

### User Guide / Cloud Phone

#### Request Instructions

[TOC]

Request Instructions
--------------------

* All API requests must be initiated using `POST`.
* All request bodies should be in `JSON` format. Please set the request header `Content-Type` to `application/json`.
* There are two verification methods, including key verification and token verification.
* Per API rate limit: 200 requests per minute, 24,000 requests per hour，After exceeding the limit, this API will be restricted for 2 hours, and it will be automatically unblocked after 2 hours.

### Token verification

When making a request, only carry the following request headers

- `traceId`: Use `Version 4 UUID`
- `Authorization` Set to `Bearer <The token value obtained from the client>`

Response Instructions

### Key verification

#### Required Request Headers for Verification

* `appId`: Team AppId
* `traceId`: Unique request ID
* `ts`: Timestamp in milliseconds
* `nonce`: Random number
* `sign`: Signature result

#### Verification Parameter Generation Method

* `traceId`: Use `Version 4 UUID`
* `nonce`: Use the first 6 characters of `traceId`
* `sign`: Concatenate the string `TeamAppId` + `traceId` + `ts` + `nonce` + `TeamApiKey`, then generate the `SHA256` hexadecimal uppercase digest of the string.

#### Example of Required Request Headers for Verification

Assuming the team's ApiKey is `YOUR_API_KEY_HERE` (example placeholder; in real GeeLark docs this is a sample 30-char key), the request headers would be set as follows:

* `appId`: `eH6gQR4oHr3FsZpI36La01IW`
* `traceId`: `db6094ab-3797-4186-84d5-b0b58eebad56`
* `ts`: `1716972892166`
* `nonce`: `db6094`
* `sign`: `6280C080AF7C3CCE168F15C913E3444A00A618CB0E16038EED9811D6E3366BDD`

---------------------

When the response code is `200`, the response body will be in `JSON` format.

### Response Object Fields

* `traceId`: Unique request ID.
* `code`: Processing result code, `0` indicates success, any other value indicates failure.
* `msg`: Processing result description.
* `data`: Data. Details are as follows:
 * On successful request: returns response data.
 * On failed request: returns the reason for failure.
 * On partially successful request: returns response data and reason for failure.

### Processing Result Code Explanation

`0` indicates success, any other value indicates failure. If an error code appears, try modifying the request based on the prompt. If the issue persists, please contact customer service and provide the `appId`, `traceId`, and the response content. Apart from global error codes, error codes specific to each API are documented in their respective descriptions. Global error codes are as follows:

* `40000`: Unknown error, please contact customer service if this occurs.
* `40001`: Failed to read request body, please contact customer service if this occurs.
* `40002`: The `traceId` in the request header cannot be empty.
* `40003`: Signature verification failed.
* `40004`: Request parameter validation failed.
* `40005`: Requested resource does not exist.
* `40006`: Partial success in the request, applicable to batch APIs.
* `40007`: Too many requests.The rate limit will be lifted in the next minute.
* `40008`: Invalid pagination parameters.
* `40009`: Batch processing completely failed.
* `40011`: Only for paid user.
* `41001`: Balance not enough.
* `40012`: The api had expire, please use the new api.
* `47002`: Too many concurrent requests. Please try again later.The rate limit will be lifted after two hours.

---

#### Request example

[TOC]

# Request Example

## Token verification

```js
const url = "https://openapi.geelark.com/open/v1/phone/list";

const appToken = "your appToken";

var traceUUid = "yxxyxxxxyxyxxyxxyxxxyxxxyxxyxxyx".replace(
 /[xy]/g,
 function (c) {
 var r = (Math.random() * 16) | 0, 
 v = c == "x" ? r : (r & 0x3) | 0x8; 
 return v.toString(16); 
 }
);

var traceId = traceUUid.toUpperCase();

var data = {
 page: 1,
 pageSize: 10,
 tags: ["tagNew"],
};

fetch(url, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 traceId: traceId,
 Authorization: "Bearer " + appToken,
 },
 body: JSON.stringify(data),
})
 .then((res) => res.json())
 .then((res) => {
 console.log(res);
 })
 .catch((err) => {
 console.error(err);
 });
```

## Key verification

```js
const CryptoJS = require("crypto-js");

const url = "https://openapi.geelark.com/open/v1/phone/list"; // Example request URL

const appID = "your appID"; // Your appID
const apiKey = "your apiKey"; // Your apiKey

let timestamp = new Date().getTime().toString(); // Millisecond timestamp

// Generate UUID
var traceUUid = "yxxyxxxxyxyxxyxxyxxxyxxxyxxyxxyx".replace(
 /[xy]/g,
 function (c) {
 var r = (Math.random() * 16) | 0, // Randomly generate a number between 0 and 15
 v = c == "x" ? r : (r & 0x3) | 0x8; // If c is 'y', only take one of 8, 9, a, b
 return v.toString(16); // Convert the number to a hexadecimal string
 }
);

var traceId = traceUUid.toUpperCase();

// nonce is the first 6 characters of traceId
var nonce = traceId.substring(0, 6);

var sign = CryptoJS.SHA256(appID + traceId + timestamp + nonce + apiKey)
 .toString()
 .toUpperCase();

var data = {
 page: 1,
 pageSize: 10,
};

headers = {
 "Content-Type": "application/json",
 appId: appID,
 traceId: traceId,
 ts: timestamp,
 nonce: nonce,
 sign: sign,
};

console.log(headers);

fetch(url, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 appId: appID,
 traceId: traceId,
 ts: timestamp,
 nonce: nonce,
 sign: sign,
 },
 body: JSON.stringify(data),
})
 .then((res) => res.json())
 .then((res) => {
 console.log(res);
 })
 .catch((err) => {
 console.error(err);
 });
```

---

#### Create automated tasks

[TOC]

**Create Account Management Task:** Directly call the [Add Task API](https://open.geelark.com/api/task-add).

**Create Video or Image Collection Posting Task:** First, upload the materials, then call the [Add Task API](https://open.geelark.com/api/task-add).

Creating Video or Image Collection Posting Task
-----------------------------------------------

1.  [File Upload](https://open.geelark.com/api/upload-getUrl)
    
2.  Use the `resource access URL` obtained in step 1 as the upload URL for the video or image, and then call the [Add Task API](https://open.geelark.com/api/task-add).

---

### User Guide / Browser

#### Request Instructions

[TOC]

## Overview

- Support local API functions
- All interface requests are initiated using `POST`.
- All request bodies are in `json` format. Please set the `Content-Type` request header to `application/json`.
- API rate limit: 200 times/min, 24,000 times/hour
- Token verification required
- Preparation before use:
	Check whether the client is open and logged in.

## Response Description

When the response code is `200`, the response body is `json`

### Response body object fields

- `traceId` Request unique ID.
- `code` Processing result code, 0 represents success, other codes represent failure.
- `msg` Description of the processing result.
- `data` The details are as follows:
 When the request is successful, the response data is returned.
If the request fails, the failure reason is returned.
If the request is partially successful, the response data and the failure reason are returned.

### Processing result code description

0 indicates success, and other values indicate failure.
If an error code appears, try modifying the request according to the prompts.
If the problem persists, please contact customer service for feedback.
In addition to the global error code, the error code corresponding to each interface is documented in its respective description. The global error codes are as follows:

- `40000` Unknown error. If this occurs, please contact customer service.
- `40001` Failed to read the request body. If this occurs, please contact customer service.
- `40002` The `traceId` header in the request cannot be empty.
- `40003` Signature verification failed.
- `40004` Request parameter verification failed.
- `40005` The requested resource does not exist.
- `40006` The request was partially successful. This applies to batch interfaces.
- `40007` Requests are too frequent. The rate limit will be lifted in the next minute.
- `40008` Pagination parameter error.
- `40009` All batch processing failed.
- `40011` Only for paid users.
- `41001` Insufficient balance.
- `40012` The interface has expired. Please use the latest interface.
- `47002` The number of concurrent requests is too high. Please try again later.
- `40014` Requests are too frequent. The rate limit will be lifted in two hours.
- `90000` Request parameter verification failed.
- `90001` User not logged in
- `90004` The user does not have browser API permissions.

---

#### Request example

[TOC]

## Example

```js
const url = "http://localhost:40185/api/v1/browser/start"; // Sample request address

const appToken = "your appToken";

var data = {
 "id": "123456789xxxx"
};

fetch(url, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 "Authorization": "Bearer " + appToken,
 },
 body: JSON.stringify(data),
})
 .then((res) => res.json())
 .then((res) => {
 console.log(res);
 })
 .catch((err) => {
 console.error(err);
 });
```

---

### Cloud Phone API / Cloud Phone Management

#### Create new V2

[TOC]

## API Description

- The Basic plan supports the creation of only one cloud phone at a time, while the Pro plan supports batch creation.
- Supports model selection. Please first call the cloud phone brand list API to obtain supported brand model information.
- Proxy information, added proxy, dynamic proxy must specify one, added proxy is used first, followed by proxy information.

## Request URL

- `https://openapi.geelark.com/open/v1/phone/addNew`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| mobileType | Yes | string | Cloud phone type, can be set</br>Android 9</br>Android 10</br>Android 11</br> Android 12</br> Android 13</br> Android 14</br> Android 15</br>Android 16 | Android 10 |
|chargeMode|No|integer|Billing mode, 0-on-demand, 1-monthly, default is on-demand|0|
|region|No|string|Specify the computer room where the cloud phone is located. Optional parameters: cn(China), sgp(Singapore), us(United States, only Android 15 is supported)| cn|
|data|Yes|array[EnvRowApi]|Environment parameter array, up to 100|Reference Request Example|

### Environment parameter <EnvRowApi>

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|profileName|Yes|string|Cloud Phone Name|myPhone|
|proxyInformation|No|string|Proxy information, supports http, https, socks5 types|socks5://AD00xx004:3000xxx0002@100.200.200.100:30000|
|refreshUrl|No|string|Proxy refresh url|http://someaddr|
|proxyQueryChannel|No|integer|Proxy detection channel, takes effect when using proxyInformation, 1-ip-api, 2-IP2Location, default is 2|2|
|proxyNumber|No|integer|The serial number of the added proxy|1|
|dynamicProxy|No|string|Saved dynamic proxy, can be set IPHTML/kookeey/Luminati(BrightData)/rolaip/Proxyma/DECODO/NodeMaven/kookeeyMobile|NodeMaven|
|dynamicProxyLocation|No|string| Dynamic proxy country, required when specifying a dynamic proxy. Please refer to [the list of dynamic proxy country codes for possible values.](https://singapore-upgrade.geelark.com/apiResource/proxy-country.txt) | us |
| mobileRegion | No | string | Cloud phone region. If not specified, it will follow the proxy. Please refer to [Cloud Phone Region List](https://singapore-upgrade.geelark.com/apiResource/region.txt) | USA-US |
| mobileProvince | No | string | State. Only the United States is currently supported. Please refer to [State-City Mapping Table](https://singapore-upgrade.geelark.com/apiResource/timezone.json)| Alabama |
| mobileCity | No | string | City. Only the United States is currently supported. Please refer to [State-City Mapping Table](https://singapore-upgrade.geelark.com/apiResource/timezone.json)| Abbeville |
|mobileLanguage|No|string|The language of the cloud phone. If you set baseOnIP, it will be based on the proxy settings. If you set default or do not set it, it will be in English. For custom language values, please refer to the [Language List](https://singapore-upgrade.geelark.com/apiResource/language.txt).|default|
|profileGroup|No|string|Group name, if it does not exist, create a new one automatically|myGroup|
|profileTags|No|array[string]|Tag name, if it does not exist, create a new one automatically|Reference Request Example |
|profileNote|No|string|Remark|remark|
| surfaceBrandName | No | string | Mobile phone brand, obtain the value corresponding to the Android version from the [brand list API](https://open.geelark.com/api/phone-brand-list "brand list API"), and the brand model should be transmitted at the same time | samsung |
| surfaceModelName | No | string | Mobile phone model, obtain the value corresponding to the Android version from the [brand list API](https://open.geelark.com/api/phone-brand-list "brand list API"), and the brand model should be transmitted at the same time | Galaxy S23 |
| netType | No | integer | Networking. 0-Wi-Fi, 1-Mobile. Only supported on Android 12/Android 13/Android 15. Default to mobile network | 0 |
| phoneNumber | No | string | Mobile phone number, automatically generated if empty | +66817806147 |
| phoneName | No | string | Device name, automatically generated by default, not supported in Android 9/11. | myDevice |



## Request Example
```json
{
  "mobileType": "Android 12",
  "chargeMode": 0,
  "data": [
    {
      "profileName": "myPhone",
      "proxyInformation": "socks5://AD00xx004:3000xxx0002@100.200.200.100:30000",
	  "proxyQueryChannel": 1,
      "mobileLanguage": "default",
      "profileGroup": "myGroup",
      "profileTags": ["myTag"],
      "profileNote": "remark"
    }
  ]
}
```


## Response Example

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "totalAmount": 1,
        "successAmount": 1,
        "failAmount": 0,
        "details": [
            {
                "index": 1,
                "code": 0,
                "msg": "success",
				"id": "497652752864775437",
                "profileName": "22 ungrouped",
                "envSerialNo": "22",
				"equipmentInfo": {
					"countryName": "Thailand",
					"phoneNumber": "+66877382166",
					"enableSim": 1,
					"imei": "863406055475987",
					"osVersion": "Android 11.0",
					"wifiBssid": "1C:1D:67:B1:C1:76",
					"mac": "9C:A5:C0:5F:C5:AD",
					"bluetoothMac": "D0:15:4A:5B:7E:AE",
					"timeZone": "Asia/Bangkok"
			 	}
            }
        ]
    }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of cloud phones created |
| successAmount | integer | Number of successful creations |
| failAmount | integer | Number of failed creations |
| details | array | Creation response details |

### details Creation Response

| Parameter Name | Type | Description |
| --- | --- | --- |
| index | integer | Creation index |
| code | integer | Result code, 0 for success |
| msg | string | Result message |
| id | string | Cloud phone ID |
| profileName | string | Cloud phone name |
| envSerialNo | string | Cloud phone serial number |
| equipmentInfo  | EquipmentInfo    | cloud phone equipment info |

#### equipmentInfo Cloud phone equipment info <EquipmentInfo>

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| countryName | string | country name |
| phoneNumber | string | phone number |
| enableSim | integer | is Sim enable : 0 unable 1 enable |
| imei | string | IMEI |
| osVersion | string | system version |
| wifiBssid | string | Wi-Fi MAC Address |
| mac | string | phone Wi-Fi MAC Address |
| bluetoothMac | string | bluetooth Mac Address |
| timeZone | string | timezone |
|deviceBrand|string|brand|
|deviceModel|string|model|

## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 44001 | Batch creation is not allowed, please upgrade to the Pro plan |
| 44002 | Batch creation is not allowed, cloud phone creation limit reached for the plan |
| 44004 | Batch creation is not allowed, maximum daily cloud phone creation limit reached |
| 43029 | The selected cloud phone model is under maintenance, please try again later |
| 45005 | Incorrect time zone setting on the cloud phone |
| 50000 | Unknown error |

---

#### Get all cloud phones

[TOC]

## API Description

Retrieve the list of cloud phones.

## Request URL

* `https://openapi.geelark.com/open/v1/phone/list`

## Request Method

* POST

## Request Parameters

### Pagination Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | No | integer | Page number, minimum is 1 | 1 |
| pageSize | No | integer | Number of records per page, minimum is 1, maximum is 100 | 10 |

### Query Parameters (Ignored if empty)

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | No | array[string] | Cloud phone ID array，The maximum length of the array is 100. If the array is not empty, these two parameters： page pageSize, will not take effect | ["5213214343124321"] |
| serialName | No | string | Cloud phone name | test |
| remark | No | string | Cloud phone remark | test |
| groupName | No | string | Cloud phone group name | test group |
| tags | No | array\[string\] | List of cloud phone tag names | See example |
| chargeMode | No | integer | charge mode | 0 pay per minute, 1 monthly subscription; If this field is left empty, all charge mode will be queried. | 
| openStatus        |  no     |   integer  | Power state  | 0 Close；1 On |
| proxyIds        |  no     |  array[string]   | List of proxy IDs. The maximum array length is 10. |  ["5213214343124321"]  |
| serialNos        |  no     |  array[string]   | List of cloud phone serial number. The maximum array length is 100. |  ["238"]  |

## Request Example
``` json
{
    "page":1,
    "pageSize":10,
    "serialName": "test",
    "remark":"",
    "groupName":"",
	"tags":[
		"tag1",
		"tag2"
	],
	"openStatus" : 1,
	"proxyIds": ["602943680722009770"],
	"serialNos": ["238"]
}
```

### Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of cloud phones |
| page | integer | Page number |
| pageSize | integer | Page size |
| items | array\[Phone\] | List of cloud phones |

### items Cloud Phone Data <Phone>

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Cloud phone ID |
| serialName | string | Cloud phone name |
| serialNo | string | Cloud phone serial number |
| group | Group | Cloud phone group information |
| remark | string | Cloud phone remark |
| status | integer | Cloud phone status<br/>0 - Started<br/>1 - Starting<br/>2 - Shut down |
| tags | array\[Tag\] | List of cloud phone tags |
| equipmentInfo  | EquipmentInfo    | cloud phone equipment info |
| proxy | Proxy | Proxy info |
| chargeMode | integer | charge mode: 0 pay per minute, 1 monthly subscription| 
| hasBind | bool | Is the device bound to a monthly subscription |
| monthlyExpire | integer | Monthly subscription expiration time, timestamp in seconds |
| rpaStatus | integer | Whether RPA is running: 1 = running, 0 = not running |

### group Group Information <Group>

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Group ID |
| name | string | Group name |
| remark | string | Group remark |

### tags Cloud Phone Tags <Tag>

| Parameter Name | Type | Description |
| --- | --- | --- |
| name | string | Cloud phone tag name |

### equipmentInfo Cloud phone equipment info <EquipmentInfo>

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| countryName | string | country name, please refer to the [Country Name Reference Table](https://material.geelark.com/t_region.xls) |
| phoneNumber | string | phone number |
| enableSim | integer | is Sim enable : 0 unable 1 enable |
| imei | string | IMEI |
| osVersion | string | system version |
| wifiBssid | string | Wi-Fi MAC Address |
| mac | string | phone Wi-Fi MAC Address |
| bluetoothMac | string | bluetooth Mac Address |
| timeZone | string | timezone |
|deviceBrand|string|brand|
|deviceModel|string|model|
|deviceName|string|Device name| 
|netType|integer|Network type: 0 – Wi-Fi, 1 – Mobile network| 
|language|string|Cloud phone language| 
|province|string|Province; only populated if specified at creation time| 
|city|string|City; only populated if specified at creation time|

### proxy Proxy info <Proxy>

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| type | string | Proxy type (socks5, http, https) |
| server | string | Proxy server |
| port | integer | Proxy port|
| username | string | Proxy username |
| password | string | Proxy password |

## Response Example
```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 1,
        "page": 1,
        "pageSize": 10,
        "items": [
            {
                "id": "123456ABCDEF",
                "serialName": "test",
                "serialNo": "1",
                "group": {
                    "id": "123456ABCDEF",
                    "name": "test group",
                    "remark": "group remark"
                },
                "remark": "env remark",
				"status": 0,
                "tags": [
					{"name": "hi"},
					{"name": "test"}
				],
				"equipmentInfo": {
					"countryName": "Thailand",
					"phoneNumber": "+66877382166",
					"enableSim": 1,
					"imei": "863406055475987",
					"osVersion": "Android 11.0",
					"wifiBssid": "1C:1D:67:B1:C1:76",
					"mac": "9C:A5:C0:5F:C5:AD",
					"bluetoothMac": "D0:15:4A:5B:7E:AE",
					"timeZone": "Asia/Bangkok",
					"deviceName": "",
                    "netType": 1,
                    "language": "en-US",
                    "province": "",
                    "city": ""
				 },
				"proxy": {
					"type": "socks5",
					"server": "129.129.129.129",
					"port": 30000,
					"username": "user",
					"password": "pass"
				}
            }
        ]
    }
}
```

## Error Codes

Error codes can be found in the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Query status

[TOC]

## API Description

Retrieve the status of cloud phones.

## Request URL

*   `https://openapi.geelark.com/open/v1/phone/status`

## Request Method

*   POST

## Request Parameters

### Query Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | List of cloud phone IDs, Limit to 100 elements | See request example |

## Request Example

```json
{
    "ids":[
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF"
    ]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of requested IDs |
| successAmount | integer | Total number of successful responses |
| failAmount | integer | Total number of failed responses |
| successDetails | array\[SuccessDetails\] | Information about successful responses |
| failDetails | array\[FailDetails\] | Information about failed responses |

### successDetails Success Information <SuccessDetails>

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | ID of the successful cloud phone |
| serialName | string | Name of the successful cloud phone |
| status | integer | Cloud phone status code<br/> 0 - Started<br/> 1 - Starting<br/> 2 - Shut down<br/> 3 - Expired |

### failDetails Failure Information <FailDetails>

| Parameter Name | Type | Description |
| --- | --- | --- |
| code | integer | Failure code 42001: Cloud phone does not exist |
| id | string | ID of the failed cloud phone |
| msg | string | Failure message |

## Response Example

```json
{
    "code": 0,
    "msg": "成功",
    "traceId": "123456ABCDEF",
    "data": {
        "totalAmount": 4,
        "successAmount": 3,
        "failAmount": 1,
        "successDetails": [
            {
                "id": "123456ABCDEF",
                "serialName": "name1",
                "status": 0
            },
            {
                "id": "123456ABCDEF",
                "serialName": "name2",
                "status": 1
            },
            {
                "id": "123456ABCDEF",
                "serialName": "name3",
                "status": 1
            }
        ],
        "failDetails": [
            {
                "code": 42001,
                "id": "123456ABCDEF",
                "msg": "env not found"
            }
        ]
    }
}
```

## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |

---

#### Start cloud phone

[TOC]

## API Description

Batch start cloud phones.

## Request URL

* `https://openapi.geelark.com/open/v1/phone/start`

## Request Method

* POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | List of cloud phone IDs, maximum 200 | See request example |
|width | No | integer | Cloud phone display width in px | Default: 336 (allowed range: 200<=width<=600)|
|center|No|integer|Whether the cloud phone display is centered|0: not centered, 1: centered; default is 1 if not provided|
|energySavingMode|No|integer|Whether to enable energy-saving mode. When enabled, the cloud phone will automatically shut down after 30 minutes of inactivity.|0: Disabled, 1: Enabled; default is 0 if not provided|
|materialTagIds|No|array[string]|Material tag ID array, supporting up to 10 elements. When this parameter is provided, the Cloud Phone Library opened by the API will only display materials corresponding to the specified tags. If omitted or empty, all materials are shown by default. This parameter requires [OEM permissions](https://open.geelark.com/api/phone-customization) to take effect.|["611460279938623025"]|

## Request Example

```json
{
    "ids":[
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF"
    ]
}
```

## Response Example

```json
{
    "code": 0, 
    "msg": "success", 
    "traceId": "12345678ABCDEF", 
    "data": {
        "totalAmount": 3, 
        "successAmount": 1, 
        "failAmount": 2, 
        "failDetails": [
            {
                "code": 43004, 
                "id": "12345678ABCDEFG", 
                "msg": "env is expired"
            }, 
            {
                "code": 42001, 
                "id": "12345678ABCDEFG", 
                "msg": "env not found"
            }
        ], 
        "successDetails": [
            {
                "id": "12345678ABCDEFG", 
                "url": "https://speedup.geelark.com/phone-api", 
                "chargingMethod": "Per-minute usage"
            }
        ]
    }
}

```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of requested IDs |
| successAmount | integer | Number of successful starts |
| successDetails | array[SuccessDetails] | Information about successed |
| failAmount | integer | Number of failed starts |
| failDetails | array[FailDetails] | Information about failures |

### SuccessDetails Successed Information

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | ID of the cloud phone |
| url | string | remote url, can be opened and visit cloud phone via Browser directly |
| chargingMethod | string | Billing type, Per-minute usage, Monthly rental, Parallels |

### FailDetails Failure Information

| Parameter Name | Type | Description |
| --- | --- | --- |
| code | integer | Failure code |
| id | string | ID of the failed cloud phone |
| msg | string | Failure message |



## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 43004 | Cloud phone has expired |
| 47004 | Device associated with cloud phone does not exist |
| 43007 | Cloud phone is already in use by another user |
| 45002 | Cloud phone proxy is unavailable |
| 47002 | Cloud phone resources are insufficient |
| 43020 | Cloud phone is currently unavailable, please try again later |
| 43029 | The selected cloud phone model is under maintenance, please try again later |

---

#### Stop cloud phone

[TOC]

## API Description

Batch shut down cloud phones.

## Request URL

*   `https://openapi.geelark.com/open/v1/phone/stop`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | List of cloud phone IDs, maximum 200 | See request example |

## Request Example

```json
{
    "ids":[
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF",
        "123456ABCDEF"
    ]
}
```

## Response Example

```json
{
    "code": 0,
    "msg": "成功",
    "traceId": "123456ABCDEF",
    "data": {
        "totalAmount": 4,
        "successAmount": 3,
        "failAmount": 1,
        "successDetails": [
            {
                "id": "123456ABCDEF",
                "serialName": "name1",
                "status": 0
            },
            {
                "id": "123456ABCDEF",
                "serialName": "name2",
                "status": 1
            },
            {
                "id": "123456ABCDEF",
                "serialName": "name3",
                "status": 1
            }
        ],
        "failDetails": [
            {
                "code": 42001,
                "id": "123456ABCDEF",
                "msg": "env not found"
            }
        ]
    }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of requested IDs |
| successAmount | integer | Number of successfully shut down IDs |
| failAmount | integer | Number of failed IDs |
| failDetails | array\[FailDetails\] | Information about failures |

### failDetails Failure Information <FailDetails>

| Parameter Name | Type | Description |
| --- | --- | --- |
| code | integer | Error code |
| id | integer | Cloud phone ID |
| msg | string | Error message |

## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 43005 | Cloud phone is executing a task |
| 43006 | Cloud phone is being remotely connected |

---

#### Delete cloud phone

[TOC]

API Description
-----------------

Batch Delete Cloud Phones

Request URL
-----------

* `https://openapi.geelark.com/open/v1/phone/delete`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | List of cloud phone IDs, Limit to 100 elements | Refer to the request example |

Request Example
---------------
```json
{
    "ids":[
        "123456ABCDEF",
        "123456ABCDEF"
    ]
}
```

Response Data Description
-------------------------

| Parameter | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of requested IDs |
| successAmount | integer | Total number of successful IDs |
| failAmount | integer | Total number of failed IDs |
| failDetails | array\[FailDetails\] | Failure details |

### Failure Details <FailDetails>

| Parameter | Type | Description |
| --- | --- | --- |
| code | integer | Error code |
| id | integer | Cloud phone ID |
| msg | string | Error message |

Response Example
----------------

```json
{
    "code": 0,
    "msg": "success",
    "traceId": "12345ABCDEF",
    "data": {
        "totalAmount": 4,
        "successAmount": 2,
        "failAmount": 2,
        "failDetails": [
            {
                "code": 42001,
                "id": "12345ABCDEF",
                "msg": "env not found"
            },
            {
                "code": 43009,
                "id": "12345ABCDEF",
                "msg": "env is started"
            }
        ]
    }
}
```

Error Codes
-----------

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 43009 | Cloud phone is started, cannot delete |
| 43010 | Cloud phone is starting, cannot delete |
| 43021 | The cloud phone is in use, please try again later |

---

#### Get GPS 

[TOC]

## Interface Description

- Query the GPS information of cloud phones, including latitude and longitude.

## Request URL

- `https://openapi.geelark.com/open/v1/phone/gps/get`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description               | Example           |
| -------------- | -------- | ------------- | ------------------------- | ----------------- |
| ids            | Yes      | array[string] | List of cloud phone IDs   | Refer to Request Example |

## Request Example

```json
{
    "ids": [
        "528086321789535232"
    ]
}
```

## Response Example

```json
{
    "traceId": "81CA3BD0B7BBB924A1C6B836B298ADA7",
    "code": 0,
    "msg": "success",
    "data": {
        "totalAmount": 1,
        "successAmount": 1,
        "failAmount": 0,
        "list": [
            {
                "id": "528086321789535232",
                "latitude": 1.3024300336837769,
                "longitude": 103.87545776367188
            }
        ]
    }
}
```

## Response Data Description

| Parameter Name | Type    | Description          |
| -------------- | ------- | -------------------- |
| totalAmount    | integer | Total number of requested IDs |
| successAmount  | integer | Total number of successful requests |
| failAmount     | integer | Total number of failed requests |
| list           | GPS     | GPS information      |

### list GPS Information <GPS>
| Parameter Name | Type    | Description          |
| -------------- | ------- | -------------------- |
| id             | string  | Cloud phone ID       |
| latitude       | float   | Latitude             |
| longitude      | float   | Longitude            |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 42001      | Cloud phone does not exist         |

---

#### Set GPS

[TOC]

## Interface Description
- Set/update the GPS information of cloud phones, including longitude and latitude, Not supported on Android 16 for now.
- Longitude range: `[-180.0, 180.0]`
- Latitude range: `[-90.0, 90.0]`

## Request URL
- `https://openapi.geelark.com/open/v1/phone/gps/set`

## Request Method
- POST

## Request Parameters
| Parameter Name | Required | Type       | Description           | Example           |
| -------------- | -------- | ---------- | --------------------- | ----------------- |
| list           | Yes      | array[GPS] | Cloud phone GPS info  | Refer to Request Example |

### list Cloud Phone GPS Info <GPS>
| Parameter Name | Required | Type   | Description | Example           |
| -------------- | -------- | ------ | ----------- | ----------------- |
| id             | Yes      | string | Cloud phone ID | Refer to Request Example |
| longitude      | Yes      | float  | Longitude    | Refer to Request Example |
| latitude       | Yes      | float  | Latitude     | Refer to Request Example |

## Request Example
```json
{
    "list": [
        {
            "id": "528086321789535232",
            "latitude": 1.30243,
            "longitude": 103.87546
        },
        {
            "id": "530011895768286208",
            "latitude": 11.30243,
            "longitude": 104.87546
        }
    ]
}
```

## Response Example
```json
{
    "traceId": "870AE3259C965B45A0D09C92A4EA8F81",
    "code": 0,
    "msg": "success",
    "data": {
        "totalAmount": 2,
        "successAmount": 2,
        "failAmount": 0
    }
}
```

### Response Data Description
| Parameter Name | Type    | Description          |
| -------------- | ------- | -------------------- |
| totalAmount    | integer | Total number of requested IDs |
| successAmount  | integer | Total number of successful requests |
| failAmount     | integer | Total number of failed requests |

## Error Codes
Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 42001      | Cloud phone does not exist         |
| 43012      | Latitude/longitude range error     |

---

#### Modify cloud phone information

[TOC]


## Interface Description

###  Warning: Do not operate this api while calling the API to start the cloud phone.

- Modify cloud phone information.
- Support modifying the cloud phone name.
- Support modifying the cloud phone remark.
- Support modifying the cloud phone tags.
- Support modifying the cloud phone proxy configuration.
- Support modifying the cloud phone group.
- Support modifying the cloud phone charge mode.
- Support modifying the cloud phone number ( It needs to be in a shutdown state)

## Request URL

- `https://openapi.geelark.com/open/v1/phone/detail/update`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| -------------- | -------- | ------------- | ------------------------- |
| id | Yes | string | Cloud phone ID |
| name | No | string | New cloud phone name, up to 100 characters |
| remark | No | string | New cloud phone remark, up to 1500 characters |
| groupID | No | string | New cloud phone group ID |
| tagIDs | No | array[string] | New cloud phone tag IDs |
| proxyConfig | No | Proxy | New cloud phone proxy config |
|proxyQueryChannel|No|integer|Proxy detection channel, takes effect when using proxyConfig, 1-ip-api, 2-IP2Location, default is 2|
| proxyId | No | string | Proxy Id |
|chargeMode|No|integer|Billing mode, 0-on-demand, 1-monthly, default is on-demand|0|
| phoneNumber | No | string | custom phone number |

### proxyConfig Static Proxy Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| typeId | Yes | integer | Proxy type ID | 1 |
| server | Yes | string | Proxy server hostname | server.com |
| port | Yes | integer | Proxy server port | 1234 |
| username | Yes | string | Proxy server username | user |
| password | Yes | string | Proxy server password | password |

### proxyConfig Dynamic Proxy Parameters

Dynamic proxy settings can be configured on the client side first, and then by setting useProxyCfg to true, you can use the already configured information without needing to provide the host, port, and other details again.

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| useProxyCfg | Yes | bool | Whether to use the already configured proxy | true |
| typeId | Yes | integer | Proxy type ID | 20 |
| protocol | No | integer | Proxy protocol type: 1 for SOCKS5, 2 for HTTP. | 1 |
| server | No | string | Proxy server hostname | server.com |
| port | No | integer | Proxy server port | 1234 |
| username | No | string | Proxy server username | user |
| password | No | string | Proxy server password | password |
| country | No | string | country, Please refer to [the list of dynamic proxy country codes for possible values.](https://singapore-upgrade.geelark.com/apiResource/proxy-country.txt) | us |
| region | No | string | region, Please refer to the corresponding proxy: [Country Codes](https://singapore-upgrade.geelark.com/apiResource/proxies-country-codes.txt) | Please fill it out based on the proxy you’re using |
| city | No | string | city, Please refer to the corresponding proxy: [Country Codes](https://singapore-upgrade.geelark.com/apiResource/proxies-country-codes.txt) | Please fill it out based on the proxy you’re using |


### typeId List
### 1. Static Proxy List

* `1` : socks5
* `2` : http
* `3` : https

### 2. Dynamic Proxy List

- `21` IPHTML
- `22` kookeey
- `23` Lumatuo(BrightData)
- `24` Proxyma
- `25` SmartProxy
- `26` RolaIP
- `27` NodeMaven
- `29` KookeeyMobile

## Request Example

```json
{
 "id": "528086284158239744",
 "name": "api update",
 "remark": "api remark",
 "tagIDs": ["528989565877355520", "528989565877289984"],
 "groupID": "528995439832269824",
 "proxyQueryChannel": 1,
 "proxyConfig": {
 "typeId": 1,
 "server": "123.123.123.123",
 "port": 32080,
 "username": "username",
 "password": "password"
 },
 "proxyId": "528989565877355520"
}
```

## Response Example

Success Response

```json
{
 "traceId": "B04B0843BD86D9589AB3BAB6A9EA3D92",
 "code": 0,
 "msg": "success"
}
```

If some tags in the tag list do not exist, there will be `failDetails` data; if none of the tags exist, the request will directly return an error, with the `code` details as shown in the **Error Codes** section below.

```json
{
 "traceId": "8B38AA778DBCD9519FB9B00D8A593DB3",
 "code": 0,
 "msg": "success",
 "data": {
 "failDetails": [
 {
 "code": 43022,
 "id": "52898956587728998",
 "msg": "tag not found"
 }
 ]
 }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| -------------- | ----------------- | -------------------------- |
| failDetails | array[FailDetails] | Tag addition failure info |

### failDetails Tag Addition Failure Info <FailDetails>

| Parameter Name | Type | Description |
| -------------- | ------- | ----------- |
| code | integer | Error code |
| id | integer | Tag ID |
| msg | string | Error msg |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| ---------- | ---------------------------------- |
| 42001 | Cloud phone does not exist |
| 43022 | Tag does not exist |
| 43032 | Group does not exist |
| 45003 | Proxy region not allowed |
| 45004 | Proxy check failed, check config |
| 45008 | Proxy type not allow |

---

#### One-click new machine V2

[TOC]

API Description
-----------------

- Generate a new cloud phone, Applications and data will be cleared

Request URL
-----------

* `https://openapi.geelark.com/open/v2/phone/newOne`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Cloud Phone ID | See request example |
| changeBrandModel | No | bool | Whether to randomize the brand and model. true: randomize, false: keep unchanged; if not provided, it remains randomize. | true |
| keepNetType | No | bool | Preserve network connection type, defaults to false, random network connection type | true |
| keepPhoneNumber | No | bool | Preserve phone number, defaults to false, random phone number | true |
| keepRegion | No | bool | Preserve region, defaults to false, follow proxy | true |
| keepLanguage | No | bool | Preserve language, defaults to false, use English | true |

Request Example
---------------

```json
{
    "id": "528715748189668352"
}
```

Response Example
----------------

```json
{
 "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
 "code": 0,
 "msg": "success"
}
```
## Error Codes


Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).


| Error Code | Description |
| --- | --- |
| 42001 | cloud phone not exist |
| 44004 | maximum daily cloud phone creation limit reached |
| 43005 | cloud phone is executing task |
| 43006 | cloud phone is occupied by remote |
| 43015 | this cloud phone is not support One-click new machine |
| 45004 | proxy detect fail |
| 43038 | the equipment brand and model have been deleted. |

---

#### Clone cloud phone

[TOC]

## API Description
- Generate a new cloud phone of the same model, retains the country, time zone, language, and GPS information. Applications and data will be cleared.

## Request URL

- `https://openapi.geelark.com/open/v1/phone/clone`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| --- | --- | --- | --- | --- |
|envId|Yes|string|The ID of the cloud phone to be cloned|
|amount|Yes|integer|The number of clones, ranging from 1 to 100|
|groupId|No|string|The ID of the target group. If not specified, the phone will be placed in an ungrouped area|
|cloneName|No|bool|Whether to clone the name|
|cloneRemark|No|bool|Whether to clone the remark|
|cloneTag|No|bool|Whether to clone the tag|
|cloneProxy|No|bool|Whether to clone the proxy|
|cloneNetType|No|bool|Whether to clone the network type|

## Request Example

```json
{
    "envId": "590711571886417452",
	"amount": 1,
    "groupId": "590711571886417453"
}
```

## Response Body Data Description

| Parameter Name       |     Type   |     Description    |
| ----------- | -----------|----------- |
| ids | array[string] | Cloned cloud phone ID|

## Response Example

```json
{
    "traceId": "B3DAFF64A7BD493CB1169D94A22BFC8D",
    "code": 0,
    "msg": "success",
    "data": {
        "ids": [
            "590711571886417454"
        ]
    }
}
```

## Error Codes

The following are API-specific error codes. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 44001 | Pro Package Limit |
| 42001 | Corresponding Cloud Machine Does Not Exist |
| 43032 | Group Does Not Exist |
| 44002 | Package Environment Quantity Limit Reached |
| 44004 | Today's Environment Creation Limit Reached |
| 44006 | Insufficient Cloud Phone Inventory |
| 43038 | Device Model Deleted |

---

#### Screen Shot

Please refer to Callback Example[TOC]

## API Description
Get a screen shot from cloud phone

## Request URL

- `https://openapi.geelark.com/open/v1/phone/screenShot`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | clound phone id | Refer to request example  |


## Request Example
```json
{
    "id": "528715748189668352"
}
```



## Response Example

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "taskId": "1850726441252569088"
    }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| taskId | string | task id |


## Error Codes


The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)


| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 42002 | Cloud phone is not running |


Callback Result and Example
---------------------------

Please refer to Callback Example

---

#### Get screen shot result

[TOC]

## API Description
Query the status of cloud phone screenshot task
After requesting a screenshot, you can actively obtain the result through this interface within 30 minutes. If it expires, the retrieval will fail

## Request URL

- `https://openapi.geelark.com/open/v1/phone/screenShot/result`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string | task id | Refer to request example |


## Request Example
```json
{
    "taskId": "528715748189668352"
}
```



## Response Example

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "status": 2,
		"downloadLink": "https://zx-cloud-phone-pre.obs.cn-southwest-2.myhuaweicloud.com/envirFileExport/1851511129017700352/IMG_20241122160248.png?AccessKeyId=UFNIPAPFJX2MAGMFGRYZ&Expires=1732264377&Signature=dqV5JYzYDdm0wwAgkZIpDrs%2FL%2FE%3D"
    }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| status | integer | 0 Acquisition failed；1 In progress；2 Execution succeeded；3 Execution failed |
| downloadLink | downloadLink | screen shot download link |


## 错误码

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Set Root Status

[TOC]

## API Description
Set root status, please start the cloud phone before setting root status.

## Request URL

- `https://openapi.geelark.com/open/v1/root/setStatus`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes |array[string] | List of cloud phone IDs ( currently supports Android 12,13,14,15,16) | Refer to request example |
| open | Yes | bool | open/close | false |


## Request Example
```json
{
    "ids" : [
        "526209711930868736"
    ],
    "open" : true
}
```



## Response Example

```json
{
    "traceId": "A24A3089958A4BC28E8B89B3AE1A61AC",
    "code": 0,
    "msg": "success",
	"data": {
        "items": [
            {
                "code": 42002,
                "msg": "phone is not running",
                "id": "543483007558772199"
            },
            {
                "code": 0,
                "msg": "success",
                "id": "543483063829554663"
            }
        ]
    }
}
```


## Error Codes

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 42001 | cloud phone not found |
| 42002 | cloud phone is not running |
| 43016 | this cloud phone does not support root |

---

#### Get device ID

[TOC]

## API Description
- Get the cloud phone device ID (please re-obtain the latest ID after one-click new phone), which corresponds to the cloud phone's unique hardware device ID, which is equivalent to the system's Andorid_ID. The App can bind to the cloud phone environment by obtaining this ID on the cloud phone. How to obtain the device ID on the App side:
Android 13 system: execute the getprop ro.boot.serialno command through adb
Other systems: execute the getprop ro.serialno command through adb

```java
if(android.os.Build.VERSION.SDK_INT == 33){
   serialNo = Command.exeCommand("getprop ro.boot.serialno");
}else {
   serialNo = Command.exeCommand("getprop ro.serialno");
}
```

## Request URL

- `https://openapi.geelark.com/open/v1/phone/serialNum/get`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | clound phone id | Refer to request example  |

## Request Example
```json
{
    "id": "528715748189668352"
}
```

## Response Example

```json
{
    "traceId": "89D8C3C08DA4DB5089069D34A3786494",
    "code": 0,
    "msg": "success",
    "data": {
        "serialNum": "r2cbvzlx5bs"
    }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| serialNum | string | cloud phone device ID |

## Error Codes


The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)


| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |

---

#### Send SMS to cloud phone

[TOC]

API Documentation
-----------------

* Send SMS to cloud phone. Before sending, please start the cloud phone first.

Request URL
-----------

* `https://openapi.geelark.com/open/v1/phone/sendSms`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Cloud phone environment ID (Currently supports only Android 12 , 13, 14, 15 devices) | 526209711930868736 |
| phoneNumber | Yes | string | Phone number | +17723504471 |
| text | Yes | string | SMS content | xxxx |

Request Example
---------------


```json
{
 "id": "526209711930868736",
 "phoneNumber": "+17723504471",
 "text": "your tk code: 6666"
}
```
----------------

```json
{
 "traceId": "9E681400B2983A5390F4B7C8BF1BF2B7",
 "code": 0,
 "msg": "success",
 "data": {}
}
```

| Error Code | Description |
| --- | --- |
| 52001 | This type of cloud phone does not support sending SMS. |

---

#### List of cloud mobile phone brands

[TOC]

## API Description

- Get a list of cloud phone brands

## Request URL

- `https://openapi.geelark.com/open/v1/phone/brand/list`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| androidVer | Yes | integer | android version, 10-16 | 10 |

## Request Example

```json
{
	"androidVer" : 10
}
```


## Response Example

```json
{
	"traceId": "B0BA8FF29AB60B8ABF4E9A26BF08F7B9",
	"code": 0,
	"msg": "success",
	"data": [
		{
			"surfaceBrandName": "samsung",
			"surfaceModelName": "Galaxy S20+"
		}
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| surfaceBrandName | string | mobile phone brand|
| surfaceModelName | string | mobile phone model|

Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

#### Transfer Cloud Phone

[TOC]

## API Description

- Transfer Cloud Phone

## Request URL

- `https://openapi.geelark.com/open/v1/phone/transfer`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| account | yes | string | target account | Anna@geelark.com |
| ids | yes | array[string] | The maximum length limit for the array of the cloud phone ID to be transferred is 200, and any part exceeding 200 will be ignored | |
| transferOption | no | arrry[string] |Transfer options with optional parameters：name：cloud phone name，proxy：cloud phone proxy，tag：cloud phone tag，remark：cloud phone remark，files：cloud phone files | [ "name","proxy", "tag","remark" ]| 

## Request Example

```json
{
    "ids": [
        "539893235657500146"
    ],
    "account": "Anna@geelark.com",
    "transferOption": [
        "name",
        "proxy",
        "tag",
        "remark"
    ]
}
```


## Response Example

```json
{
	"traceId": "B0BA8FF29AB60B8ABF4E9A26BF08F7B9",
	"code": 0,
	"msg": "success",
	"data": [
		{
			"successCount": 10,
			"failCount": 2,
			"failEnvIds" : ["539893235657500146"]
		}
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| successCount | integer | success count|
| failCount | integer | fail count|
| failEnvIds | array[string] | transfer failed cloud phone id (currently in use or does not exist)|


Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)


| Error Code | Description |
| --- | --- |
| 40013 | target account not found |
| 43022 | can not transfer to myself |

---

#### Set net type

[TOC]

## API Description

Set up the cloud phone network connection mode

## Request URL


- `https://openapi.geelark.com/open/v1/phone/net/set`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description                 |
| ----------- | ---- | ------------- | -------------------- |
| id          | Yes   | string        | Cloud Phone ID            |
| netType | Yes | integer | Networking. 0-Wi-Fi, 1-Mobile. Only supported on Android 12/Android 13/Android 15 |


## Request Example


```json
{
  "id": "528086284158239744",
  "netType": 0
}
```


## Response Example


```json
{
  "traceId": "B04B0843BD86D9589AB3BAB6A9EA3D92",
  "code": 0,
  "msg": "success"
}
```

## Error Codes

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 42001 | cloud phone not found |

---

#### Hide Accessibility

[TOC]

## API Description

- Hide the cloud phone accessibility in app.
- Currently supports Android 12, 13, 15 devices.
- It will overwrite the old configuration

## Request URL

- `https://openapi.geelark.com/open/v1/phone/hideAccessibility`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array[string] | clound phone id array | ["599257164413959866"] |
| pkgName | Yes | array[string] | app package name array |  ["com.zhiliaoapp.musically"] |

## Request Example

```json
{
	"ids": ["599257164413959866"],
	"pkgName" : ["com.zhiliaoapp.musically"]
}
```

## Response Data Description
### failDetails 
| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| id | integer   | cloud phone id  |
| code | integer   | error code  |
| msg | string   | error msg  |

## Response Example

```json
{
	"traceId": "A17A45A3B3A49AB5A1BDB654B7C82B81",
	"code": 0,
	"msg": "success",
	"data": {
		"failDetails": [
			{
				"id": "599257164413959866",
				"code": 42001,
				"msg": "env not found"
			}
		]
	}
}
```

## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | cloud phone not exist |
| 43037 | does not support this devices |

---

#### Move Group

\[TOC\]

API Description
---------------

Move Group

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/moveGroup`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envIds | Yes | array\[string\] | Array of cloud phone IDs, supports up to 100 elements | See request example |
| groupId | Yes | string | Group ID. Pass `"0"` to move to the ungrouped category | See request example |

Request Example
---------------
```json
{
    "envIds": [
        "601876382020062634"
    ],
    "groupId": "590711571886417453"
}
```
Response Example
----------------
```json
{
    "traceId": "B3DAFF64A7BD493CB1169D94A22BFC8D",
    "code": 0,
    "msg": "success"
}
```

---

#### Batch Import Contacts

[TOC]

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/importContacts`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| id | Yes | string | Cloud phone ID |
| contacts | Yes | array[ContactObject] | Array of contact information |

### ContactObject
| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| email1 | No | string | Email 1 |
| email2 | No | string | Email 2 |
| fax | No | string | Fax number. At least one of **mobile**, **work**, or **fax** must be non-empty |
| firstName | No | string | First name. At least one of **firstName** or **lastName** must be non-empty |
| lastName | No | string | Last name. At least one of **firstName** or **lastName** must be non-empty |
| mobile | No | string | Mobile phone number. At least one of **mobile**, **work**, or **fax** must be non-empty |
| work | No | string | Work phone number. At least one of **mobile**, **work**, or **fax** must be non-empty |

Request Example
---------------
```json
{
	"id":"557536075321468390",
	"contacts": [
		{
			"firstName": "jay",
			"mobile": "13288888888"
		}
	]
}
```

Response Example
----------------
```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

## Response Body Data Description
|Parameter	|Type|	Description|
| ----------- | -----------|----------- |
|taskId	|string	|Task ID (valid for query one hour after the task is created)|

---

#### Get Batch Import Contacts Result

[TOC]

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/importContactsResult`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string | Task ID | See request example |

Request Example
---------------

```json
{
    "taskId": "528715748189668352"
}
```
Response Example
----------------

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "status": 2
    }
}
```

Response Body Data Description
------------------------------

| Parameter | Type | Description |
| --- | --- | --- |
| status | integer | Task status: 1 = In progress, 2 = Successful, 3 = Failed |

---

#### Get cloud phone network settings

[TOC]

## API Description

Obtain cloud phone network settings, including access to blacklists.

## Request URL

- `https://openapi.geelark.com/open/v1/phone/netConfig/get`

## Request Method

- POST

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| blackList |  array[string] | Accessing blacklisted domains |

## Response Example

```json
{
    "traceId": "B3DAFF64A7BD493CB1169D94A22BFC8D",
    "code": 0,
    "msg": "success",
	"data": {
		"blackList": ["c.com"]
	}
}
```

---

#### Modify cloud phone network settings

[TOC]

## API Description

Modify cloud phone network settings, including access blacklist

### Access Blacklist

Maximum three blacklisted domains. Settings take effect immediately; the cloud phone will be unable to access domains on the blacklist.

Only supports Android 9/10/11/12/13/15 cloud phones.

## Request URL

- `https://openapi.geelark.com/open/v1/phone/netConfig/set`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| --- | --- | --- | --- |
| blackList | No | array[string] | If a blacklisted domain is accessed, the list will not be updated unless an array is passed; otherwise, the list will be set to null. |


## Request Example
```json
 {
	"blackList": ["c.com"]
}
```

## Response Example

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success"
}
```

---

#### Cloud Phone API / Automation / Task Management

##### Query task

[TOC]

## API Description

Task Query

## Request URL

* `https://openapi.geelark.com/open/v1/task/query`

## Request Method

* POST

## Request Parameters

### Query Parameters (Ignore if empty)

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | Array of task IDs, up to 100 | See request example |

## Request Example


```json
{
    "ids": ["123321", "456654"]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of tasks |
| items | array\[Task\] | Array of tasks |

### Task

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Task ID |
| planName | string | Task plan name |
| taskType | integer | Task type<br>1 TikTok video posting<br>2 TikTok AI account warmup<br>3 TikTok carousel posting<br>4 TikTok account login<br>6 TikTok profile editing<br>42 Custom(Including Facebook, YouTube and other platforms) |
| serialName | string | Cloud phone name |
| envId | string | Cloud phone ID |
| scheduleAt | integer | Scheduled time, timestamp in seconds |
| status | integer | Task status<br>1 Waiting<br>2 In progress<br>3 Completed<br>4 Failed<br>7 Cancelled |
| failCode | integer | Failure code, refer to task failure codes and reasons |
| failDesc | string | Failure reason, refer to task failure codes and reasons |
| cost | integer | The time a task takes to complete or fail (in seconds)|
| shareLink | string | Share link |

### Task Failure Codes and Reasons

| Failure Code | Failure Reason |
| - | - |
| 20002 | The machine is performing other tasks |
| 20003 | Execution timeout. Please view the publication on TikTok. |
| 20005 | Task canceled |
| 20006 | The same task was canceled |
| 20007 | Unsupported task type |
| 20008 | Failed because the APP language was modified. You need to change the APP language to English and run it again. |
| 20100 | No network connection |
| 20101 | Agent parameter error |
| 20102 | Failed to set modification parameters |
| 20103 | Failed to restart device |
| 20104 | After successful login, an error occurs when saving login information to the service. |
| 20105 | Installation of tiktok failed |
| 20106 | Failed to install 163 mailbox |
| 20107 | Unable to load video |
| 20108 | No network connection |
| 20109 | Setting proxy via interface failed |
| 20110 | Failed to obtain proxy ip |
| 20111 | Installation of auxiliary apk failed |
| 20112 | Failed to start secondary apk |
| 20113 | The IP address is the same before and after setting the proxy |
| 20114 | The node_addr field is parsed into an entity class error |
| 20115 | Check login failure |
| 20116 | The account is not logged in |
| 20117 | No email account and password |
| 20118 | Failed to obtain IP before setting proxy |
| 20119 | Failed to bind NetService |
| 20120 | Failed to obtain tiktok cookie |
| 20121 | Failed to obtain tiktokInfo |
| 20122 | Failed to start tiktok |
| 20123 | Failed to obtain geoip |
| 20124 | The waiting time to enter the homepage is too long |
| 20125 | Login failed, too many attempts |
| 20126 | Login failed, email not found |
| 20127 | Login failed when switching to email username |
| 20128 | Login failure |
| 20129 | Device offline |
| 20130 | Account password is wrong |
| 20131 | Too many attempts |
| 20132 | Login loading time exceeds 2 minutes |
| 20133 | Slider loading time is too long |
| 20134 | No network when verifying slider |
| 20135 | Failed to obtain tiktok UserName |
| 20136 | Account blocked |
| 20137 | The account has been blocked and you can appeal. |
| 20138 | The circular verification code slider takes too long to load |
| 20139 | Circle slider validation failed |
| 20140 | Slider verification fails to obtain screenshots |
| 20141 | There is no network during circular verification |
| 20142 | Graphic validation failed |
| 20143 | Maximum number of attempts reached |
| 20144 | Incorrect account or password |
| 20145 | Your account has repeatedly violated community guidelines |
| 20200 | Failed to download file, please check the network or try again later |
| 20201 | Failed to upload video, please check whether the network is smooth or try again later |
| 20202 | Failed to upload the video. It has been 0% for five minutes. Please check the network or try again later. |
| 20203 | Failed to upload video, failed for 15 minutes, please check the network or try again later |
| 20204 | Video upload was rejected |
| 20205 | Failed to click the capture button on the main page |
| 20206 | Failed to upload when clicking on the album page |
| 20207 | Album file type click failed |
| 20208 | Failed to download the video file. The specified download file was not found. Please check the network or try again later. |
| 20209 | Failed to select video |
| 20210 | Album next step failed |
| 20211 | Next step of preview page failed |
| 20212 | Preview completed and click Next failed. |
| 20213 | Clicking Publish on the publish page fails |
| 20214 | Clicking Publish Now failed |
| 20215 | Preview completed and waiting for video processing failed |
| 20216 | Failed to push stream to camera |
| 20217 | Recording video from camera failed |
| 20218 | Green screen filter not found |
| 20219 | Failed to switch rear camera |
| 20220 | Download video file connection is empty |
| 20221 | Couldn't decode. select anther video |
| 20222 | Video sound is not available |
| 20223 | Can't select Stickers |
| 20224 | Stickers list not found |
| 20225 | Stickers list failed to load |
| 20226 | Failed to download MENTION stickers |
| 20227 | MENTION sticker input box not found |
| 20228 | Publish video@user list failed to load |
| 20229 | The specified user was not found |
| 20230 | Handle video timeout |
| 20231 | Add link control not found |
| 20232 | Add product control not found |
| 20233 | Failed to enter product page |
| 20234 | Product not found |
| 20235 | Modify product name control not found |
| 20236 | Failed to add product |
| 20237 | Product sold out |
| 20238 | Video source is not set for push streaming |
| 20239 | Audio source is not set for push streaming |
| 20240 | Camera recording video waiting timeout |
| 20241 | Product unavailable |
| 20242 | Failed to jump to video details |
| 20243 | Failed to click the Use Music button |
| 20244 | Video music removed |
| 20245 | Timeout waiting for video to load |
| 20246 | Video ID does not exist |
| 20247 | Failed to switch seconds |
| 20248 | Search button not found |
| 20249 | Product URL input box not found |
| 20250 | Add product button not found |
| 20251 | Video publishing failed, saved to drafts |
| 20252 | Background music infringement |
| 20253 | Background music is muted causing failure |
| 20254 | Failed to set default audience |
| 20255 | Your account is permanently restricted from selling products |
| 20256 | Failed to enter product title editing page |
| 20257 | Video upload timed out |
| 20258 | Element not found |
| 20259 | Mention user not found |
| 20260 | Mention user button not found |
| 20261 | User search not found |
| 20262 | When entering the product page, it prompts that there is no network connection. |
| 20263 | Product name contains inappropriate words |
| 20264 | Account temporarily restricted |
| 20265 | Shooting the same video had special effects, causing the mission to fail. |
| 20266 | Failed to add product name, please check whether the product name is compliant |
| 20300 | Registration slider verification failed |
| 20301 | Registration circular verification failed to obtain screenshots |
| 20302 | Failed to enter email verification code |
| 20303 | The email verification code was not found within the specified time. |
| 20304 | Failed to register account and create new password |
| 20305 | Failed to jump to homepage via email |
| 20306 | No clickable registration button found |
| 20307 | Date of birth is illegal or failed to obtain |
| 20308 | Registration failed by clicking on the email address |
| 20309 | Failed to enter email |
| 20310 | The next step after clicking to enter the email address fails. |
| 20311 | The next step after clicking Create Password fails. |
| 20312 | Verification countdown not found |
| 20313 | Resend verification code not found |
| 20314 | Failed to start mailbox app |
| 20315 | Verification code sent too many times |
| 20316 | Skip creation of username failed |
| 20317 | TikTok prompts you to try too many times when registering |
| 20318 | Email login failed |
| 20319 | Email login failed, account locked |
| 20320 | Email login failed, account password is wrong |
| 20321 | Email login failed |
| 20322 | Login password control not found |
| 20323 | Waiting too long after entering the verification code |
| 20324 | Account or password incorrect |
| 20325 | Fail to register |
| 20326 | Account has been registered |
| 20327 | Waiting too long after entering the verification code |
| 20328 | An error message appears after entering the password |
| 20329 | Email verification is required but currently only supports 163 email addresses |
| 20330 | Email is registered |
| 20331 | Birthday next step failed |
| 20332 | Determine the registration entrance failed |
| 20333 | Circular verification code processing exception |
| 20334 | Email verification required |
| 20335 | An exception occurred during registration |
| 20336 | Email verification code execution failed |
| 20337 | The email verification code has expired or timed out |
| 20338 | The input box control for filling in the email verification code was not found. |
| 20339 | The email verification code decoding interface returns an invalid verification code. |
| 20340 | Interests selection failed |
| 20401 | Failed to jump to me |
| 20402 | Failed to click to edit information |
| 20403 | Unable to edit data |
| 20501 | Failed to jump to user page |
| 20502 | There is no network when jumping to the user page |
| 20503 | The specified user could not be found |
| 20504 | An exception occurred when jumping to the user page |
| 20505 | Fan list page failed to load |
| 20506 | Fan list page loading timeout |
| 20507 | Fan list loading timeout |
| 20508 | Failed to load more fans list |
| 20601 | Failed to click window option |
| 20602 | Failed to jump to showcase page |
| 20603 | Failed to jump to add product page |
| 20604 | Failed to enter product URL page |
| 20605 | Failed to enter product URL |
| 20606 | Failed to add product |
| 20607 | This account does not have a shopping cart |
| 20700 | Unsupported type |
| 20701 | Failed to open developer tools |
| 20702 | TikTok Shop button does not exist |
| 20703 | Failed to enter TikTok Shop |
| 20704 | Failed to open shopping cart |
| 20705 | Failed to enter the invitation page |
| 20706 | Agree to invitation page exception |
| 20707 | Failed to click to agree to the invitation |
| 20708 | Invitation failed |
| 20709 | Failed to enter revenue page |
| 20710 | Authorization revenue page exception |
| 20711 | Authorization revenue failed |
| 20712 | Access data authorization failed |
| 20713 | Data authorization failed |
| 20714 | Failed to detect shopping cart permissions |
| 20715 | Click Account Settings Failed |
| 20801 | @ button not found |
| 20802 | List element not found |
| 20803 | No users mentioned were found |
| 20804 | Edit input box not found |
| 20901 | No delete button found |
| 21001 | Top button not found |
| 20267 | Custom template task publishing failed |
| 29995 | Currently unavailable; maintenance in progress |
| 29996 | Proxy detection failed |
| 29997 | Insufficient balance |
| 29998 | The cloud phone has been deleted |
| 29999 | Unknown error |

## Response Example

### Task Completed

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 1,
        "items": [
            {
                "id": "123456ABCDEF",
                "planName": "plan123456ABCDEF",
                "taskType": 2,
                "serialName": "test",
                "envId": "123456654321",
                "scheduleAt": 1718744459,
                "status": 3
            }
        ]
    }
}
```

### Task Failed

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 1,
        "items": [
            {
                "id": "123456ABCDEF",
                "planName": "plan123456ABCDEF",
                "taskType": 2,
                "serialName": "test",
                "envId": "123456654321",
                "scheduleAt": 1718744459,
                "status": 4,
				"failCode": 29999,
				"failDesc": "some reason"
            }
        ]
    }
}
```

Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

##### Batch query tasks

[TOC]

## API Description

Query all tasks scheduled within the past 7 days.

## Request URL

* `https://openapi.geelark.com/open/v1/task/historyRecords`

## Request Method

* POST

## Request Parameters

### Query Parameters (Ignore if empty)

| Parameter   | Required | Type   | Description                       | Example               |
| --- | --- | --- | --- | --- |
| size         | No       | integer     | Number of records per page, maximum is 100 | 100                   |
| lastId       | No       | string | The `id` of the last item from the previous page’s `data.items` array | "574376043897425896" |
| ids | No | array[string] | Task IDs, maximum 100 | ["574376043897425896"] |

## Request Example

```json
{
 "size": 10,
 "lastId": "574376043897425896"
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of tasks |
| items | array\[Task\] | Array of tasks |

### Task

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Task ID |
| planName | string | Task plan name |
| taskType | integer | Task type<br>1 TikTok video posting<br>2 TikTok AI account warmup<br>3 TikTok carousel posting<br>4 TikTok account login<br>6 TikTok profile editing<br>42 Custom(Including Facebook, YouTube and other platforms) |
| serialName | string | Cloud phone name |
| envId | string | Cloud phone ID |
| scheduleAt | integer | Scheduled time, timestamp in seconds |
| status | integer | Task status<br>1 Waiting<br>2 In progress<br>3 Completed<br>4 Failed<br>7 Cancelled |
| failCode | integer | Failure code, refer to task failure codes and reasons |
| failDesc | string | Failure reason, refer to task failure codes and reasons |
| cost | integer | The time a task takes to complete or fail (in seconds)|

### Task Failure Codes and Reasons

| Failure Code | Failure Reason |
| - | - |
| 20002 | The machine is performing other tasks |
| 20003 | Execution timeout. Please view the publication on TikTok. |
| 20005 | Task canceled |
| 20006 | The same task was canceled |
| 20007 | Unsupported task type |
| 20008 | Failed because the APP language was modified. You need to change the APP language to English and run it again. |
| 20100 | No network connection |
| 20101 | Agent parameter error |
| 20102 | Failed to set modification parameters |
| 20103 | Failed to restart device |
| 20104 | After successful login, an error occurs when saving login information to the service. |
| 20105 | Installation of tiktok failed |
| 20106 | Failed to install 163 mailbox |
| 20107 | Unable to load video |
| 20108 | No network connection |
| 20109 | Setting proxy via interface failed |
| 20110 | Failed to obtain proxy ip |
| 20111 | Installation of auxiliary apk failed |
| 20112 | Failed to start secondary apk |
| 20113 | The IP address is the same before and after setting the proxy |
| 20114 | The node_addr field is parsed into an entity class error |
| 20115 | Check login failure |
| 20116 | The account is not logged in |
| 20117 | No email account and password |
| 20118 | Failed to obtain IP before setting proxy |
| 20119 | Failed to bind NetService |
| 20120 | Failed to obtain tiktok cookie |
| 20121 | Failed to obtain tiktokInfo |
| 20122 | Failed to start tiktok |
| 20123 | Failed to obtain geoip |
| 20124 | The waiting time to enter the homepage is too long |
| 20125 | Login failed, too many attempts |
| 20126 | Login failed, email not found |
| 20127 | Login failed when switching to email username |
| 20128 | Login failure |
| 20129 | Device offline |
| 20130 | Account password is wrong |
| 20131 | Too many attempts |
| 20132 | Login loading time exceeds 2 minutes |
| 20133 | Slider loading time is too long |
| 20134 | No network when verifying slider |
| 20135 | Failed to obtain tiktok UserName |
| 20136 | Account blocked |
| 20137 | The account has been blocked and you can appeal. |
| 20138 | The circular verification code slider takes too long to load |
| 20139 | Circle slider validation failed |
| 20140 | Slider verification fails to obtain screenshots |
| 20141 | There is no network during circular verification |
| 20142 | Graphic validation failed |
| 20143 | Maximum number of attempts reached |
| 20144 | Incorrect account or password |
| 20145 | Your account has repeatedly violated community guidelines |
| 20200 | Failed to download file, please check the network or try again later |
| 20201 | Failed to upload video, please check whether the network is smooth or try again later |
| 20202 | Failed to upload the video. It has been 0% for five minutes. Please check the network or try again later. |
| 20203 | Failed to upload video, failed for 15 minutes, please check the network or try again later |
| 20204 | Video upload was rejected |
| 20205 | Failed to click the capture button on the main page |
| 20206 | Failed to upload when clicking on the album page |
| 20207 | Album file type click failed |
| 20208 | Failed to download the video file. The specified download file was not found. Please check the network or try again later. |
| 20209 | Failed to select video |
| 20210 | Album next step failed |
| 20211 | Next step of preview page failed |
| 20212 | Preview completed and click Next failed. |
| 20213 | Clicking Publish on the publish page fails |
| 20214 | Clicking Publish Now failed |
| 20215 | Preview completed and waiting for video processing failed |
| 20216 | Failed to push stream to camera |
| 20217 | Recording video from camera failed |
| 20218 | Green screen filter not found |
| 20219 | Failed to switch rear camera |
| 20220 | Download video file connection is empty |
| 20221 | Couldn't decode. select anther video |
| 20222 | Video sound is not available |
| 20223 | Can't select Stickers |
| 20224 | Stickers list not found |
| 20225 | Stickers list failed to load |
| 20226 | Failed to download MENTION stickers |
| 20227 | MENTION sticker input box not found |
| 20228 | Publish video@user list failed to load |
| 20229 | The specified user was not found |
| 20230 | Handle video timeout |
| 20231 | Add link control not found |
| 20232 | Add product control not found |
| 20233 | Failed to enter product page |
| 20234 | Product not found |
| 20235 | Modify product name control not found |
| 20236 | Failed to add product |
| 20237 | Product sold out |
| 20238 | Video source is not set for push streaming |
| 20239 | Audio source is not set for push streaming |
| 20240 | Camera recording video waiting timeout |
| 20241 | Product unavailable |
| 20242 | Failed to jump to video details |
| 20243 | Failed to click the Use Music button |
| 20244 | Video music removed |
| 20245 | Timeout waiting for video to load |
| 20246 | Video ID does not exist |
| 20247 | Failed to switch seconds |
| 20248 | Search button not found |
| 20249 | Product URL input box not found |
| 20250 | Add product button not found |
| 20251 | Video publishing failed, saved to drafts |
| 20252 | Background music infringement |
| 20253 | Background music is muted causing failure |
| 20254 | Failed to set default audience |
| 20255 | Your account is permanently restricted from selling products |
| 20256 | Failed to enter product title editing page |
| 20257 | Video upload timed out |
| 20258 | Element not found |
| 20259 | Mention user not found |
| 20260 | Mention user button not found |
| 20261 | User search not found |
| 20262 | When entering the product page, it prompts that there is no network connection. |
| 20263 | Product name contains inappropriate words |
| 20264 | Account temporarily restricted |
| 20265 | Shooting the same video had special effects, causing the mission to fail. |
| 20266 | Failed to add product name, please check whether the product name is compliant |
| 20300 | Registration slider verification failed |
| 20301 | Registration circular verification failed to obtain screenshots |
| 20302 | Failed to enter email verification code |
| 20303 | The email verification code was not found within the specified time. |
| 20304 | Failed to register account and create new password |
| 20305 | Failed to jump to homepage via email |
| 20306 | No clickable registration button found |
| 20307 | Date of birth is illegal or failed to obtain |
| 20308 | Registration failed by clicking on the email address |
| 20309 | Failed to enter email |
| 20310 | The next step after clicking to enter the email address fails. |
| 20311 | The next step after clicking Create Password fails. |
| 20312 | Verification countdown not found |
| 20313 | Resend verification code not found |
| 20314 | Failed to start mailbox app |
| 20315 | Verification code sent too many times |
| 20316 | Skip creation of username failed |
| 20317 | TikTok prompts you to try too many times when registering |
| 20318 | Email login failed |
| 20319 | Email login failed, account locked |
| 20320 | Email login failed, account password is wrong |
| 20321 | Email login failed |
| 20322 | Login password control not found |
| 20323 | Waiting too long after entering the verification code |
| 20324 | Account or password incorrect |
| 20325 | Fail to register |
| 20326 | Account has been registered |
| 20327 | Waiting too long after entering the verification code |
| 20328 | An error message appears after entering the password |
| 20329 | Email verification is required but currently only supports 163 email addresses |
| 20330 | Email is registered |
| 20331 | Birthday next step failed |
| 20332 | Determine the registration entrance failed |
| 20333 | Circular verification code processing exception |
| 20334 | Email verification required |
| 20335 | An exception occurred during registration |
| 20336 | Email verification code execution failed |
| 20337 | The email verification code has expired or timed out |
| 20338 | The input box control for filling in the email verification code was not found. |
| 20339 | The email verification code decoding interface returns an invalid verification code. |
| 20340 | Interests selection failed |
| 20401 | Failed to jump to me |
| 20402 | Failed to click to edit information |
| 20403 | Unable to edit data |
| 20501 | Failed to jump to user page |
| 20502 | There is no network when jumping to the user page |
| 20503 | The specified user could not be found |
| 20504 | An exception occurred when jumping to the user page |
| 20505 | Fan list page failed to load |
| 20506 | Fan list page loading timeout |
| 20507 | Fan list loading timeout |
| 20508 | Failed to load more fans list |
| 20601 | Failed to click window option |
| 20602 | Failed to jump to showcase page |
| 20603 | Failed to jump to add product page |
| 20604 | Failed to enter product URL page |
| 20605 | Failed to enter product URL |
| 20606 | Failed to add product |
| 20607 | This account does not have a shopping cart |
| 20700 | Unsupported type |
| 20701 | Failed to open developer tools |
| 20702 | TikTok Shop button does not exist |
| 20703 | Failed to enter TikTok Shop |
| 20704 | Failed to open shopping cart |
| 20705 | Failed to enter the invitation page |
| 20706 | Agree to invitation page exception |
| 20707 | Failed to click to agree to the invitation |
| 20708 | Invitation failed |
| 20709 | Failed to enter revenue page |
| 20710 | Authorization revenue page exception |
| 20711 | Authorization revenue failed |
| 20712 | Access data authorization failed |
| 20713 | Data authorization failed |
| 20714 | Failed to detect shopping cart permissions |
| 20715 | Click Account Settings Failed |
| 20801 | @ button not found |
| 20802 | List element not found |
| 20803 | No users mentioned were found |
| 20804 | Edit input box not found |
| 20901 | No delete button found |
| 21001 | Top button not found |
| 20267 | Custom template task publishing failed |
| 29995 | Currently unavailable; maintenance in progress |
| 29996 | Proxy detection failed |
| 29997 | Insufficient balance |
| 29998 | The cloud phone has been deleted |
| 29999 | Unknown error |

## Response Example

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 1,
        "items": [
            {
                "id": "123456ABCDEF",
                "planName": "plan123456ABCDEF",
                "taskType": 2,
                "serialName": "test",
                "envId": "123456654321",
                "scheduleAt": 1718744459,
                "status": 3
            }
        ]
    }
}
```

Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

##### Cancel task

[TOC]

## API Description

You can call this interface to cancel tasks that are in the following status:

*   `Waiting for execution`
- `In progress`

## Request URL

*   `https://openapi.geelark.com/open/v1/task/cancel`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| --- | --- | --- | --- |
| ids | Yes | array\[string\] | A task ID array, with a maximum of 100 entries. |

## Request Example

```json
{
    "ids": ["123321", "456654"]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number processed |
| successAmount | integer | Number of successfully processed tasks |
| failAmount | integer | Number of failed tasks |
| failDetails | array\[FailDetail\] | Details of failed tasks |

### FailDetail

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Task ID |
| code | integer | Error code |
| msg | string | Error message |

## Response Examples

### All Success

```json
{
    "traceId": "123456ABCEDF",
    "code": 0,
    "msg": "success",
	"data": {
		"totalAmount": 10,
		"successAmount": 10,
		"failAmount": 0
	}
}
```
### All Fail

```json
{
    "traceId": "123456ABCEDF",
    "code": 40000,
    "msg": "unknown error"
}
```
or
```json
{
    "traceId": "123456ABCEDF",
    "code": 40009,
    "msg": "process all failure",
	"data": {
		"totalAmount": 1,
		"successAmount": 0,
		"failAmount": 1,
		"failDetails": [
			"id": "123456ABCEDF"
			"code": "48001",
			"msg": "the current task status does not allow the operation"
		]
	}
}
```

### Partial Success

```json
{
    "traceId": "123456ABCEDF",
    "code": 40006,
    "msg": "partial success",
	"data": {
		"totalAmount": 2,
		"successAmount": 1,
		"failAmount": 1,
		"failDetails": [
			"id": "123456ABCEDF"
			"code": "48001",
			"msg": "the current task status does not allow the operation"
		]
	}
}
```

## Error Codes

For outer-layer response error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

## Single Task Processing Error Codes

| Error Code | Description |
| --- | --- |
| 48001 | Task status does not allow cancellation |
| 40000 | Unknown error |

---

##### Retry Task

[TOC]

## API Description

A task can be retried up to 5 times.  
Tasks created by the client will automatically retry up to 2 times if they fail, while tasks created via the API will not automatically retry.  
If the task still fails after automatic retries, this interface can be called to retry the task.  
The interface can be called to retry the task when the task is in the following states:

*   `Task Failed`
*   `Task Canceled`

## Request URL

*   `https://openapi.geelark.com/open/v1/task/restart`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| --- | --- | --- | --- |
| ids | Yes | array\[string\] | Array of task IDs |

## Request Example

```json
{
    "ids": ["123321", "456654"]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total number of tasks processed |
| successAmount | integer | Number of tasks processed successfully |
| failAmount | integer | Number of tasks failed to process |
| failDetails | array\[FailDetail\] | Details of failed tasks |

### FailDetail

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Task ID |
| code | integer | Error code |
| msg | string | Error message |

## Response Examples

### All Successful

```json
{
    "traceId": "123456ABCEDF",
    "code": 0,
    "msg": "success",
	"data": {
		"totalAmount": 10,
		"successAmount": 10,
		"failAmount": 0
	}
}
```

### All Failed


```json
{
    "traceId": "123456ABCEDF",
    "code": 40000,
    "msg": "unknown error"
}
```
or
```json
{
    "traceId": "123456ABCEDF",
    "code": 40009,
    "msg": "process all failure",
	"data": {
		"totalAmount": 1,
		"successAmount": 0,
		"failAmount": 1,
		"failDetails": [
			"id": "123456ABCEDF"
			"code": "48001",
			"msg": "the current task status does not allow the operation"
		]
	}
}
```
### Partial Success

```json
{
    "traceId": "123456ABCEDF",
    "code": 40006,
    "msg": "partial success",
	"data": {
		"totalAmount": 2,
		"successAmount": 1,
		"failAmount": 1,
		"failDetails": [
			"id": "123456ABCEDF"
			"code": "48001",
			"msg": "the current task status does not allow the operation"
		]
	}
}
```

## Error Codes

For outer response error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

### Single Task Processing Error Codes

| Error Code | Description |
| --- | --- |
| 40005 | Environment has been deleted |
| 48000 | Task retry limit reached |
| 48001 | Task status does not allow retry |
| 48002 | Task does not exist |
| 48003 | The task resource has expired |

---

##### Task Detail

[TOC]

## API Description

The first request for searchAfter does not need to be passed. If the response's logContinue is true, it indicates that the log needs to be returned in pages. At this point, the response's searchAfter can be passed as a parameter.

## Request URL

- `https://openapi.geelark.com/open/v1/task/detail`

## Request Method

- POST

## Request Parameters

### Query Parameters (Ignore if empty)

| Parameter Name | Required | Type | Description | Example |
| ----------- | -------| -----------|----------- |----------- |
| id       | Yes     |   string  | Task ID | 1234567898 |
| searchAfter | No | array[integer] | Log pagination parameters | Reference request example |

## Request Example

```json
{
    "id": "1234567898",
	"searchAfter": [
		1749004889852
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| id | string | Task ID |
| planName | string | Task plan name |
| taskType | integer | Task type<br>1 TikTok video posting<br>2 TikTok AI account warmup<br>3 TikTok carousel posting<br>4 TikTok account login<br>6 TikTok profile editing<br>42 Custom(Including Facebook, YouTube and other platforms) |
| serialName | string | Cloud phone name |
| envId | string | Cloud phone ID |
| scheduleAt | integer | Scheduled time, timestamp in seconds |
| status | integer | Task status<br>1 Waiting<br>2 In progress<br>3 Completed<br>4 Failed<br>7 Cancelled |
| failCode | integer | Failure code, refer to task failure codes and reasons |
| failDesc | string | Failure reason, refer to task failure codes and reasons |
| cost | integer | The time a task takes to complete or fail (in seconds)|
| resultImages | array[string] | When the task is completed or fails, take a screenshot of the information |
| logs | array[string] | Task log, with time in Zone 0, returns when the task is completed or fails |
| searchAfter | array[integer] | Log pagination parameters |
| logContinue | bool | Is there still a log |

### Task Failure Codes and Reasons

| Failure Code | Failure Reason |
| - | - |
| 20002 | The machine is performing other tasks |
| 20003 | Execution timeout. Please view the publication on TikTok. |
| 20005 | Task canceled |
| 20006 | The same task was canceled |
| 20007 | Unsupported task type |
| 20008 | Failed because the APP language was modified. You need to change the APP language to English and run it again. |
| 20100 | No network connection |
| 20101 | Agent parameter error |
| 20102 | Failed to set modification parameters |
| 20103 | Failed to restart device |
| 20104 | After successful login, an error occurs when saving login information to the service. |
| 20105 | Installation of tiktok failed |
| 20106 | Failed to install 163 mailbox |
| 20107 | Unable to load video |
| 20108 | No network connection |
| 20109 | Setting proxy via interface failed |
| 20110 | Failed to obtain proxy ip |
| 20111 | Installation of auxiliary apk failed |
| 20112 | Failed to start secondary apk |
| 20113 | The IP address is the same before and after setting the proxy |
| 20114 | The node_addr field is parsed into an entity class error |
| 20115 | Check login failure |
| 20116 | The account is not logged in |
| 20117 | No email account and password |
| 20118 | Failed to obtain IP before setting proxy |
| 20119 | Failed to bind NetService |
| 20120 | Failed to obtain tiktok cookie |
| 20121 | Failed to obtain tiktokInfo |
| 20122 | Failed to start tiktok |
| 20123 | Failed to obtain geoip |
| 20124 | The waiting time to enter the homepage is too long |
| 20125 | Login failed, too many attempts |
| 20126 | Login failed, email not found |
| 20127 | Login failed when switching to email username |
| 20128 | Login failure |
| 20129 | Device offline |
| 20130 | Account password is wrong |
| 20131 | Too many attempts |
| 20132 | Login loading time exceeds 2 minutes |
| 20133 | Slider loading time is too long |
| 20134 | No network when verifying slider |
| 20135 | Failed to obtain tiktok UserName |
| 20136 | Account blocked |
| 20137 | The account has been blocked and you can appeal. |
| 20138 | The circular verification code slider takes too long to load |
| 20139 | Circle slider validation failed |
| 20140 | Slider verification fails to obtain screenshots |
| 20141 | There is no network during circular verification |
| 20142 | Graphic validation failed |
| 20143 | Maximum number of attempts reached |
| 20144 | Incorrect account or password |
| 20145 | Your account has repeatedly violated community guidelines |
| 20200 | Failed to download file, please check the network or try again later |
| 20201 | Failed to upload video, please check whether the network is smooth or try again later |
| 20202 | Failed to upload the video. It has been 0% for five minutes. Please check the network or try again later. |
| 20203 | Failed to upload video, failed for 15 minutes, please check the network or try again later |
| 20204 | Video upload was rejected |
| 20205 | Failed to click the capture button on the main page |
| 20206 | Failed to upload when clicking on the album page |
| 20207 | Album file type click failed |
| 20208 | Failed to download the video file. The specified download file was not found. Please check the network or try again later. |
| 20209 | Failed to select video |
| 20210 | Album next step failed |
| 20211 | Next step of preview page failed |
| 20212 | Preview completed and click Next failed. |
| 20213 | Clicking Publish on the publish page fails |
| 20214 | Clicking Publish Now failed |
| 20215 | Preview completed and waiting for video processing failed |
| 20216 | Failed to push stream to camera |
| 20217 | Recording video from camera failed |
| 20218 | Green screen filter not found |
| 20219 | Failed to switch rear camera |
| 20220 | Download video file connection is empty |
| 20221 | Couldn't decode. select anther video |
| 20222 | Video sound is not available |
| 20223 | Can't select Stickers |
| 20224 | Stickers list not found |
| 20225 | Stickers list failed to load |
| 20226 | Failed to download MENTION stickers |
| 20227 | MENTION sticker input box not found |
| 20228 | Publish video@user list failed to load |
| 20229 | The specified user was not found |
| 20230 | Handle video timeout |
| 20231 | Add link control not found |
| 20232 | Add product control not found |
| 20233 | Failed to enter product page |
| 20234 | Product not found |
| 20235 | Modify product name control not found |
| 20236 | Failed to add product |
| 20237 | Product sold out |
| 20238 | Video source is not set for push streaming |
| 20239 | Audio source is not set for push streaming |
| 20240 | Camera recording video waiting timeout |
| 20241 | Product unavailable |
| 20242 | Failed to jump to video details |
| 20243 | Failed to click the Use Music button |
| 20244 | Video music removed |
| 20245 | Timeout waiting for video to load |
| 20246 | Video ID does not exist |
| 20247 | Failed to switch seconds |
| 20248 | Search button not found |
| 20249 | Product URL input box not found |
| 20250 | Add product button not found |
| 20251 | Video publishing failed, saved to drafts |
| 20252 | Background music infringement |
| 20253 | Background music is muted causing failure |
| 20254 | Failed to set default audience |
| 20255 | Your account is permanently restricted from selling products |
| 20256 | Failed to enter product title editing page |
| 20257 | Video upload timed out |
| 20258 | Element not found |
| 20259 | Mention user not found |
| 20260 | Mention user button not found |
| 20261 | User search not found |
| 20262 | When entering the product page, it prompts that there is no network connection. |
| 20263 | Product name contains inappropriate words |
| 20264 | Account temporarily restricted |
| 20265 | Shooting the same video had special effects, causing the mission to fail. |
| 20266 | Failed to add product name, please check whether the product name is compliant |
| 20300 | Registration slider verification failed |
| 20301 | Registration circular verification failed to obtain screenshots |
| 20302 | Failed to enter email verification code |
| 20303 | The email verification code was not found within the specified time. |
| 20304 | Failed to register account and create new password |
| 20305 | Failed to jump to homepage via email |
| 20306 | No clickable registration button found |
| 20307 | Date of birth is illegal or failed to obtain |
| 20308 | Registration failed by clicking on the email address |
| 20309 | Failed to enter email |
| 20310 | The next step after clicking to enter the email address fails. |
| 20311 | The next step after clicking Create Password fails. |
| 20312 | Verification countdown not found |
| 20313 | Resend verification code not found |
| 20314 | Failed to start mailbox app |
| 20315 | Verification code sent too many times |
| 20316 | Skip creation of username failed |
| 20317 | TikTok prompts you to try too many times when registering |
| 20318 | Email login failed |
| 20319 | Email login failed, account locked |
| 20320 | Email login failed, account password is wrong |
| 20321 | Email login failed |
| 20322 | Login password control not found |
| 20323 | Waiting too long after entering the verification code |
| 20324 | Account or password incorrect |
| 20325 | Fail to register |
| 20326 | Account has been registered |
| 20327 | Waiting too long after entering the verification code |
| 20328 | An error message appears after entering the password |
| 20329 | Email verification is required but currently only supports 163 email addresses |
| 20330 | Email is registered |
| 20331 | Birthday next step failed |
| 20332 | Determine the registration entrance failed |
| 20333 | Circular verification code processing exception |
| 20334 | Email verification required |
| 20335 | An exception occurred during registration |
| 20336 | Email verification code execution failed |
| 20337 | The email verification code has expired or timed out |
| 20338 | The input box control for filling in the email verification code was not found. |
| 20339 | The email verification code decoding interface returns an invalid verification code. |
| 20340 | Interests selection failed |
| 20401 | Failed to jump to me |
| 20402 | Failed to click to edit information |
| 20403 | Unable to edit data |
| 20501 | Failed to jump to user page |
| 20502 | There is no network when jumping to the user page |
| 20503 | The specified user could not be found |
| 20504 | An exception occurred when jumping to the user page |
| 20505 | Fan list page failed to load |
| 20506 | Fan list page loading timeout |
| 20507 | Fan list loading timeout |
| 20508 | Failed to load more fans list |
| 20601 | Failed to click window option |
| 20602 | Failed to jump to showcase page |
| 20603 | Failed to jump to add product page |
| 20604 | Failed to enter product URL page |
| 20605 | Failed to enter product URL |
| 20606 | Failed to add product |
| 20607 | This account does not have a shopping cart |
| 20700 | Unsupported type |
| 20701 | Failed to open developer tools |
| 20702 | TikTok Shop button does not exist |
| 20703 | Failed to enter TikTok Shop |
| 20704 | Failed to open shopping cart |
| 20705 | Failed to enter the invitation page |
| 20706 | Agree to invitation page exception |
| 20707 | Failed to click to agree to the invitation |
| 20708 | Invitation failed |
| 20709 | Failed to enter revenue page |
| 20710 | Authorization revenue page exception |
| 20711 | Authorization revenue failed |
| 20712 | Access data authorization failed |
| 20713 | Data authorization failed |
| 20714 | Failed to detect shopping cart permissions |
| 20715 | Click Account Settings Failed |
| 20801 | @ button not found |
| 20802 | List element not found |
| 20803 | No users mentioned were found |
| 20804 | Edit input box not found |
| 20901 | No delete button found |
| 21001 | Top button not found |
| 20267 | Custom template task publishing failed |
| 29995 | Currently unavailable; maintenance in progress |
| 29996 | Proxy detection failed |
| 29997 | Insufficient balance |
| 29998 | The cloud phone has been deleted |
| 29999 | Unknown error |

## Response Example

### Task Completed

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
		"id": "123456ABCDEF",
		"planName": "plan123456ABCDEF",
		"taskType": 2,
		"serialName": "test",
		"envId": "123456654321",
		"scheduleAt": 1718744459,
		"status": 3,
		"cost": 60,
		"resultImages": [
            "https://material.geelark.com/geeUserUix/569544577254450679_1929760564478226432_20250604104103.jpg"
        ],
        "logs": [
            "[2025-06-04 02:38:00 025] Waiting for execution"
        ],
        "searchAfter": [
            1749004889853
        ],
        "logContinue": false
    }
}
```

### Task Failed

```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
		"id": "123456ABCDEF",
		"planName": "plan123456ABCDEF",
		"taskType": 2,
		"serialName": "test",
		"envId": "123456654321",
		"scheduleAt": 1718744459,
		"status": 4,
		"failCode": 29999,
		"failDesc": "some reason",
		"cost": 60,
		"resultImages": [
            "https://material.geelark.com/geeUserUix/569544577254450679_1929760564478226432_20250604104103.jpg"
        ],
        "logs": [
            "[2025-06-04 02:38:00 025] Waiting for execution"
        ],
        "searchAfter": [
            1749004889853
        ],
        "logContinue": false
    }
}
```

Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

#### Cloud Phone API / Automation / TikTok

##### Add video/image/warmup task

[TOC]

## API Description

* Create a warmup task by directly calling the add task interface.
* To create video or image set tasks, you need to upload the materials first, then call the add task interface.
* The warmup task created by calling this interface is not automatically retried.

## Request URL

* `https://openapi.geelark.com/open/v1/task/add`

## Request Method

* POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| planName | No | string | Task plan name, auto-generated if not provided | testAdd |
| remark | No | string | Remarks, up to 200 characters | task |
| taskType | Yes | integer | Task type<br>1 Publish video<br>2 Warmup<br>3 Publish image set | 3 |
| list | Yes | array | Task parameter array, create a maximum of 100 tasks at a time | Refer to request examples |

### Publish Video Task Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| scheduleAt | Yes | integer | Scheduled time, in seconds timestamp. If the value is less than the current time, the value is calculated based on the current time. | 1718744459 |
| envId | Yes | string | Cloud phone ID | 123456654321 |
| video | Yes | string | Video URL | https://demo.geelark.com/open-upload/DhRP36s3.mp4 , to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| videoDesc | No | string | Video description. Maximum 4000 characters | This is a video |
| productId | No | string | product id | 7498614361651,How to get the product ID: https://help.geelark.com/video-id-product-id|
| productTitle | No | string | Product display title | Title |
| refVideoId | No | string | Similar video ID | 722856939 ,How to get the video ID: https://help.geelark.com/video-id-product-id |
| maxTryTimes | No | integer | Maximum number of automatic retries. The value ranges from 0 to 3. The default value is 3 | 1 |
| timeoutMin | No | integer | Time-out period. The value ranges from 30 to 80 (unit minute). The default value is 80 | 30 |
| sameVideoVolume | No | integer | Same video volume, 0-100 | 30 |
| sourceVideoVolume | No | integer | Original video volume, 0-100 | 30 |
| markAI | No | bool | Whether to label AI generated content, default is false | false |
| cover | No | string | Video cover | https://demo.geelark.com/open-upload/DhRP36s3.jpg , to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| needShareLink | No | bool | Whether to obtain the sharing link, the default value is false | false |

### Warmup Task Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| scheduleAt | Yes | integer | Scheduled time, in seconds timestamp. If the value is less than the current time, the value is calculated based on the current time. | 1718744459 |
| envId | Yes | string | Cloud phone ID | 123456654321 |
| action | Yes | string | Warmup action<br>search profile - Search personal profile<br>search video - Search short videos<br>browse video - Randomly browse videos | browse video |
| keywords | No | array[string] | Search keyword, required when searching behavior, optional when browsing behavior | Refer to request examples |
| duration | Yes | integer | Browsing duration, in minutes | 10 |

### Publish Image Set Task Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| scheduleAt | Yes | integer | Scheduled time, in seconds timestamp. If the value is less than the current time, the value is calculated based on the current time. | 1718744459 |
| envId | Yes | string | Cloud phone ID | 123456654321 |
| images | Yes | array | Image URLs | Refer to request examples , to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)|
| videoDesc | No | string | Video description. Maximum 4000 characters | This is an image set video |
| videoId | No | string | Same video ID | 722856939 ,How to get the video ID: https://help.geelark.com/video-id-product-id|
| videoTitle | No | string | Gallery Title. Maximum 90 characters | This is a gallery title |
| productId | No | string | product id | 7498614361651,How to get the product ID: https://help.geelark.com/video-id-product-id|
| productTitle | No | string | Product display title | Title |
| maxTryTimes | No | integer | Maximum number of automatic retries. The value ranges from 0 to 3. The default value is 3 | 1 |
| timeoutMin | No | integer | Time-out period. The value ranges from 30 to 80 (unit minute). The default value is 80 | 30 |
| sameVideoVolume | No | integer | Same video volume, 0-100 | 30 |
| markAI | No | bool | Whether to label AI generated content, default is false | false |
| needShareLink | No | bool | Whether to obtain the sharing link, the default value is false | false |

## Request Examples

### Example 1: Warmup


```json
{
    "planName": "testAdd",
    "taskType": 2,
    "list": [
        {
            "scheduleAt": 1718744459,
            "envId": "123456654321",
            "action": "search video",
            "keywords": ["hi"],
			"duration": 10
        }
    ]
}
```

### Example 2: Publish Video

```json
{
    "planName": "testAdd",
    "taskType": 1,
    "list": [
        {
            "scheduleAt": 1718744459,
            "envId": "123456654321",
            "video": "https://demo.geelark.com/open-upload/DhRP36s3.mp4"
        }
    ]
}
```

### Example 3: Publish Image Set

```json
{
    "planName": "testAdd",
    "taskType": 3,
    "list": [
        {
            "scheduleAt": 1718744459,
            "envId": "123456654321",
            "images": ["https://demo.geelark.com/open-upload/DhRP36s3.jpg", "https://demo.geelark.com/open-upload/DhRP36s3.jpg"]
        }
    ]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| taskIds | array | Array of task IDs |

## Response Example

```json
{
    "traceId": "123456ABCEDF",
    "code": 0,
    "msg": "success",
	"data": {
		"taskIds": [
			"123456ABCEDF"
		]
	}
}
```
## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 41000 | Insufficient task credits |
| 43004 | Cloud phone has expired, please renew or upgrade your plan |
| 41001 | balance not enough |
| 43018 | The monthly cloud mobile phone is not bound to the monthly device |
| 48004 | The app required by the task does not meet the requirements |

---

##### TikTok login

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokLogin`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| account | Yes | string | Account, up to 64 characters |
| password | Yes | string | Password, up to 64 characters |

Request Example
----------------

```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "account":"test@gmail.com",
 "password": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok profile edit

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokEdit`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| avatar | No | string | Avatar URL, refer to the User Guide - File Upload for creating automation tasks; the uploaded image should have a 1:1 aspect ratio, otherwise the edit will fail |
| nickName | No | string | Nickname, up to 30 characters |
| bio | No | string | Bio, up to 160 characters |
| site | No | string | Website, please provide a URL starting with http/https |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "avatar":"https://singapore-upgrade.geelark.com/a.jpg",
 "nickName": "test",
 "bio":"test",
 "site":"https://www.abc.com" 
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok star

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomStar`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| likeProbability | No | int | Probability of liking, 0-100, default is 30 |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok star - Asia

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomStarAsia`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| likeProbability | No | integer | Probability of liking, 0-100, default is 30 |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok AI comment

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomComment`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| useAi | Yes | integer | Whether to use AI: 1 for AI (only available for Pro users); 2 for not using AI, provide your own comment |
| comment | Yes | string | Comment content, up to 500 characters; required when useAi is 2 |
| links | No | array[string] | Specified link |
| commentProbability | No | integer | Comment probability, 0-100, default is 30 |
| searchKeywords |  No | array[string] | Search keywords |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "useAi":2,
 "comment": "test"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok AI comment - Asia

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomCommentAsia`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| useAi | Yes | integer | Whether to use AI: 1 for AI (only available for Pro users); 2 for not using AI, provide your own comment |
| comment | Yes | string | Comment content, up to 500 characters; required when useAi is 2 |
| links | No | array[string] | Specified link |
| commentProbability | No | integer | Comment probability, 0-100, default is 30 |
| searchKeywords |  No | array[string] | Search keywords |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "useAi":2,
 "comment": "test"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Send private message on TikTok

[TOC]

Request URL
-----------

- `https://openapi.geelark.com/open/v1/rpa/task/tiktokMessage`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| usernames | Yes |array[string]|usernames |
| content | Yes |string|content. Maximum 6000 characters |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "usernames":["user"],
  "content": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Send private message on TikTok - Asia

[TOC]

Request URL
-----------

- `https://openapi.geelark.com/open/v1/rpa/task/tiktokMessageAsia`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| usernames | Yes |array[string]|usernames |
| content | Yes |string|content. Maximum 6000 characters |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "usernames":["user"],
  "content": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok follow

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomFollow`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| followProbability | Yes | integer | Pay attention to probability, 0-100|

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "followProbability": 30
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok follow - Asia

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokRandomFollowAsia`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| followProbability | Yes | integer | Pay attention to probability, 0-100|

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "followProbability":30
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Hide all TikTok videos

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokHide`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Hide all TikTok videos - Asia

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokHideAsia`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Delete all TikTok videos

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokDel`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Delete all TikTok videos - Asia

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/tiktokDelAsia`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Facebook

##### Facebook auto login

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/faceBookLogin`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| email | Yes | string | Email, up to 64 characters |
| password | Yes | string | Password, up to 64 characters |

Request Example
----------------

```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "email":"test@gmail.com",
 "password": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook auto comment

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/faceBookAutoComment`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| postAddress | Yes | string | Post address, up to 128 characters |
| comment | Yes | \[\]string | Comments, up to 10, each comment up to 8000 characters |
| keyword | Yes | \[\]string | Keywords, up to 10, each keyword up to 100 characters |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "postAddress":"https://abc.com",
 "comment": ["test1", "test2"],
 "keyword": ["k1", "k2"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook post content

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/faceBookPublish`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes | string | Title, up to 200 characters |
| video | Yes | \[\]string | Videos, up to 10 videos, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)|

Request Example
----------------

```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title":"title",
 "video": ["https://singapore-upgrade.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook maintenance

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/faceBookActiveAccount`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| browsePostsNum | Yes | integer | Estimated number of posts to browse, minimum 1, maximum 100 |
| keyword | Yes | \[\]string | Keywords, up to 10, each keyword up to 150 characters |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "postAddress":"https://abc.com",
 "browsePostsNum": 10,
 "keyword": ["k1", "k2"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook publish Reels video

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/faceBookPubReels`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| description | Yes | string | Caption, up to 500 characters |
| video | Yes | string | Video, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)|
| page | No |string|page|

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "description":"description",
 "video": "https://material.geelark.com/a.mp4"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Send private messages on Facebook

[TOC]

Request URL
-----------

- `https://openapi.geelark.com/open/v1/rpa/task/faceBookMessage`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| usernames | Yes |array[string]|usernames |
| content | Yes |string|content. Maximum 20000 characters |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "usernames":["user"],
  "content": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Instagram

##### Instagram publish Reels video

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/instagramPubReels`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| description | Yes | string | Caption, up to 2200 characters |
| video | Yes | \[\]string | Videos, up to 10, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)|
| sameStyleUrl | No | string | Same URL |
| sameStyleVoice | No | integer | Same volume, range 0-100 |
| originalVoice | No | integer | Original volume, range 0-100 |
| aiTag | No | bool | AI tag, defaults to false. |
| needShareLink | No | bool | Whether to retrieve the sharing link, the default is false. |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "description":"description",
 "video": ["https://material.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Instagram AI account warmup

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/instagramWarmup`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| browseVideo | No | integer | Number of videos viewed, 1-100 |
| keyword | No | string | Search keyword |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "browseVideo":1
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Send private messages on Instagram

[TOC]

Request URL
-----------

- `https://openapi.geelark.com/open/v1/rpa/task/instagramMessage`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| usernames | Yes |array[string]|usernames |
| content | Yes |string|content. Maximum 1000 characters |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "usernames":["user"],
  "content": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Instagram publish Reels image

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/instagramPubReelsImages`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| description | Yes | string | Caption, up to 2200 characters |
| image | Yes | \[\]string | Images, up to 10, to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| sameStyleUrl | No | string | Same URL |
| aiTag | No | bool | AI tag, defaults to false. |
| publishPost | No | bool | Posting a POST request defaults to false. |
| needShareLink | No | bool | Whether to retrieve the sharing link, the default is false. |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "description":"description",
 "image": ["https://material.geelark.com/a.jpg"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Instagram auto login

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/instagramLogin`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| account | Yes | string | Account, up to 64 characters |
| password | Yes | string | Password, up to 64 characters |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "account":"test@gmail.com",
 "password": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Edit Instagram profile

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/instagramEdit`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| profilePicture | No | array[string] | Avatar |
| nickname | No | string | Nickname |
| username | No | string | Username |
| biography | No | string | Biography |
| linkURL | No | string | Link URL |
| linkTitle | No | string | Link Title |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "nickname":"myName",
 "username": "myName"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / YouTube

##### YouTube publish Short

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/youtubePubShort`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes | string | Title, up to 100 characters |
| video | Yes | string | Video,  to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| sameStyleUrl | No | string | Same style URL, up to 500 characters |
| sameStyleVoice | Yes | integer | Same style volume, 0-100. If you do not want to send the same URL, just send 0 |
| originalVoice | Yes | integer | Original voice volume, 0-100. If you do not want to send the same URL, just send 0 |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title":"title",
 "video": "https://material.geelark.com/a.mp4",
 "SameStyleUrl": "https://www.abc.com",
 "sameStyleVoice":50,
 "originalVoice":50
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### YouTube publish Video

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/youtubePubVideo`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes | string | Title, up to 100 characters |
| description | Yes | string | Description, up to 5000 characters |
| video | Yes | string | Video,  to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)  |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title":"title",
 "description":"description",
 "video": "https://material.geelark.com/a.mp4"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### YouTube maintenance

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/youTubeActiveAccount`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| browseVideoNum | Yes | integer | Estimated number of videos to browse, minimum 1, maximum 100 |
| keyword | Yes | \[\]string | Keywords, up to 10, each keyword up to 150 characters |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "postAddress":"https://abc.com",
 "browseVideoNum": 10,
 "keyword": ["k1", "k2"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Google

##### Google auto login

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/googleLogin`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| email | Yes | string | Email, up to 64 characters |
| password | Yes | string | Password, up to 64 characters |
|code2fa|No|string|2fa code|

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "email":"test@gmail.com",
 "password": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Download apps on Google

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/googleAppDownload`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| appName | Yes |string|app name |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "appName":"TikTok"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Open the app on Google for browsing

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/googleAppBrowser`


Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| appName | Yes |string|app name |
| description | No |string|describe your experience |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "appName":"TikTok",
  "description": "good app"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Shein

##### SHEIN auto login

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/sheinLogin`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| email | Yes | string | Email, up to 64 characters |
| password | Yes | string | Password, up to 64 characters |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "email":"test@gmail.com",
 "password": "123456"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / X(Twitter)

##### Publish content on X(Twitter)

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/xPublish`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| description | Yes | string | Caption, up to 280 characters |
| video | Yes | \[\]string | Videos, up to 1, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |

Request Example
----------------
```json
{
	"name":"test",
	"remark":"test remark",
	"scheduleAt": 1741846843,
	"id":"557536075321468390",
	"description":"description",
	"video": ["https://material.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Reddit

##### Reddit AI account warmup

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/redditWarmup`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| keyword | No | string | Search keyword |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Publish video on Reddit

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/redditVideo`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes |string|Title|
| description | No |string|Description |
| video | Yes | \[\]string | Videos, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| community | Yes |string|Community |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "description":"description",
 "video": ["https://material.geelark.com/a.mp4"],
 "community": "cat"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Publish pictures and texts on Reddit

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/redditImage`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes |string|Title|
| description | No |string|Description |
| images | Yes | \[\]string | Images, to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl)|
| community | Yes |string|Community |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "description":"description",
 "images": ["https://material.geelark.com/a.jpg"],
 "community": "cat"
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Pinterest

##### Publish video on Pinterest

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/pinterestVideo`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes |string|Title. Maximum 100 characters|
| description | Yes |string|Description. Maximum 800 characters |
| video | Yes | \[\]string | Videos, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| link | No |string|Link |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "description":"description",
 "video": ["https://material.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Publish pictures and texts on Pinterest

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/pinterestImage`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes |string|Title. Maximum 100 characters|
| description | Yes |string|Description. Maximum 800 characters |
| images | Yes | \[\]string | Images, to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |
| link | No |string|Link |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "description":"description",
 "images": ["https://material.geelark.com/a.jpg"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Threads

##### Publish video on Threads

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/threadsVideo`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| topic | No | string |Topic |
| title | Yes |string|Title. Maximum 500 characters|
| video | Yes | \[\]string | Videos, to upload videos, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "video": ["https://material.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Publish pictures and texts on Threads

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/threadsImage`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| topic | No | string |Topic |
| title | Yes |string|Title. Maximum 500 characters|
| images | Yes | \[\]string | Images, to upload images, please refer to [Upload Temporary Files to GeeLark](https://open.geelark.com/api/upload-getUrl) |

Request Example
----------------
```json
{
 "name":"test",
 "remark":"test remark",
 "scheduleAt": 1741846843,
 "id":"557536075321468390",
 "title": "title",
 "images": ["https://material.geelark.com/a.jpg"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Cloud Phone API / Automation / Custom Task

##### Task flow query

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/task/flow/list`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| page | Yes | integer | Page number, minimum value is 1. |
| pageSize | Yes | integer | Number of items per page, minimum is 1, maximum is 100. |

Request Example
----------------

```json
{
	"page": 1,
	"pageSize": 1
}
```

## Response Data Description

| Field Name | Type | Description |
| ----------- | -----------|----------- |
| total | integer | Total number of items |
| page | integer | Page number |
| pageSize | integer | Number of items per page |
| items | array[TaskFlow] | Task flow array  |

### TaskFlow

| Field Name | Type | Description |
| ----------- | -----------|----------- |
| id | string   | Task flow id |
| title | string   | Task flow title |
| desc | string   | Task flow description |
| params | array[string]   | Task flow parameter field name |

Response Example
----------------

```json
{
	 "traceId": "914969A485BE1AE584ECB4D19AF83EBA",
	 "code": 0,
	 "msg": "success",
	 "data": {
		 "total": 1,
		 "page": 1,
		 "pageSize": 1,
		 "items": [
			 {
				 "id": "562316072435344885",
				 "title": "video flow",
				 "desc": "this is a video flow",
				 "params": [
					 "Title",
					 "Desc",
					 "Video"
				 ]
			 }
		 ]
	 }
}
```

---

##### Create custom task

[TOC]

API Description
-----------
Get the task flows by Task flow query API first

Request URL
-----------

* `https://openapi.geelark.com/open/v1/task/rpa/add`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| flowId | Yes | string | Task flow id(The ID field of the Task flow query response) |
| paramMap | No | object | Task flow parameters, with corresponding parameter types as follows:<br>String: string<br>Batch text: array[string]<br>Number: number<br>Boolean: bool<br>File: array[string] |

Request Example
----------------

```json
{
	"name":"test",
	"remark":"test remark",
	"scheduleAt": 1741846843,
	"id":"557536075321468390",
	"flowId": "562316072435344885",
	"paramMap": {
		"Title": "video",
		"Desc": "this is video",
		"Video": ["https://material.geelark.com/a.mp4"]
	}
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Import custom task flow

[TOC]

API Description
-----------
Import or update custom task flow

Request URL
-----------

* `https://openapi.geelark.com/open/v1/task/flow/import`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| id | no |string| custom task flow id, If the corresponding ID is passed, it will be updated; if not, a new one will be created |
| gal | no |string| custom task flow data |

Request Example
----------------

```json
{
    "id": "612345671223083526",
    "gal" : "{\"content\":{\"contents\":[{\"config\":{\"packgename\":\"com.zhiliaoapp.musically\",\"remark\":\"\",\"timeout\":30000},\"type\":\"openApp\"},{\"config\":{\"remark\":\"\",\"timeout\":10000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"filters\":[{\"content\":\"Home\",\"type\":\"text\"}],\"remark\":\"\",\"searchTime\":3000,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"\"},\"type\":\"click\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"filters\":[{\"content\":\"For You\",\"type\":\"text\"},{\"content\":\"android:id/text1\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":30,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"\"},\"type\":\"click\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"direction\":\"top\",\"distanceMax\":700,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"direction\":\"top\",\"distanceMax\":700,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"children\":[{\"config\":{\"direction\":\"top\",\"distanceMax\":600,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"filters\":[{\"content\":\"com.zhiliaoapp.musically:id/nl8\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":30,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"avatar\"},\"type\":\"waitEle\"},{\"config\":{\"children\":[{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":30000,\"timeoutMin\":10000,\"timeoutType\":\"randomInterval\"},\"type\":\"waitTime\"},{\"config\":{\"children\":[{\"config\":{\"filters\":[{\"content\":\"com.zhiliaoapp.musically:id/cf6\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":3000,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\"},\"type\":\"click\"}],\"hiddenChildren\":false,\"other\":[],\"probability\":30,\"relation\":\"random\",\"remark\":\"\"},\"type\":\"ifElse\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":30000,\"timeoutMin\":10000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"}],\"condition\":[\"avatar\"],\"hiddenChildren\":false,\"other\":[],\"relation\":\"exist\",\"remark\":\"\"},\"type\":\"ifElse\"}],\"hiddenChildren\":false,\"remark\":\"\",\"times\":15,\"variableIndex\":\"for_times_index\"},\"type\":\"forTimes\"},{\"config\":{\"remark\":\"\",\"timeout\":120000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"}],\"errorType\":\"skip\",\"isDebug\":false,\"timeOut\":\"30\",\"contentType\":\"phone\"},\"desc\":\"A TikTok Task flow\",\"title\":\"TikTok\"}"
}
```


Response Example
----------------

```json
{
    "traceId": "A9D852F29EA2CA1BA46B963DB449329A",
    "code": 0,
    "msg": "success",
    "data": {
        "id": "612345671223083526" // custom task flow id
    }
}
```

## Error Codes

For error codes, please refer to [Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 48002 | custom task flow not found |

---

##### Export custom task flow

[TOC]

API Description
-----------
Export custom task flow

Request URL
-----------

* `https://openapi.geelark.com/open/v1/task/flow/export`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| id | Yes |string| custom task flow id |

Request Example
----------------

```json
{
	"id": "612345671223083526"
}
```


Response Example
----------------

```json
{
	"traceId": "8119CCF5AD857989B62A940E8B5AA5AF",
	"code": 0,
	"msg": "success",
	"data": {
		"gal" : "{\"content\":{\"contents\":[{\"config\":{\"packgename\":\"com.zhiliaoapp.musically\",\"remark\":\"\",\"timeout\":30000},\"type\":\"openApp\"},{\"config\":{\"remark\":\"\",\"timeout\":10000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"filters\":[{\"content\":\"Home\",\"type\":\"text\"}],\"remark\":\"\",\"searchTime\":3000,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"\"},\"type\":\"click\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"filters\":[{\"content\":\"For You\",\"type\":\"text\"},{\"content\":\"android:id/text1\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":30,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"\"},\"type\":\"click\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"direction\":\"top\",\"distanceMax\":700,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"direction\":\"top\",\"distanceMax\":700,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"},{\"config\":{\"children\":[{\"config\":{\"direction\":\"top\",\"distanceMax\":600,\"distanceMin\":500,\"position\":[300,700],\"randomWheelSleepTime\":[300,500],\"remark\":\"\"},\"type\":\"scrollPage\"},{\"config\":{\"filters\":[{\"content\":\"com.zhiliaoapp.musically:id/nl8\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":30,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\",\"variable\":\"avatar\"},\"type\":\"waitEle\"},{\"config\":{\"children\":[{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":30000,\"timeoutMin\":10000,\"timeoutType\":\"randomInterval\"},\"type\":\"waitTime\"},{\"config\":{\"children\":[{\"config\":{\"filters\":[{\"content\":\"com.zhiliaoapp.musically:id/cf6\",\"type\":\"id\"}],\"remark\":\"\",\"searchTime\":3000,\"serial\":1,\"serialMax\":50,\"serialMin\":1,\"serialType\":\"fixedValue\"},\"type\":\"click\"}],\"hiddenChildren\":false,\"other\":[],\"probability\":30,\"relation\":\"random\",\"remark\":\"\"},\"type\":\"ifElse\"},{\"config\":{\"remark\":\"\",\"timeout\":2000,\"timeoutMax\":30000,\"timeoutMin\":10000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"}],\"condition\":[\"avatar\"],\"hiddenChildren\":false,\"other\":[],\"relation\":\"exist\",\"remark\":\"\"},\"type\":\"ifElse\"}],\"hiddenChildren\":false,\"remark\":\"\",\"times\":15,\"variableIndex\":\"for_times_index\"},\"type\":\"forTimes\"},{\"config\":{\"remark\":\"\",\"timeout\":120000,\"timeoutMax\":300000,\"timeoutMin\":1000,\"timeoutType\":\"fixedValue\"},\"type\":\"waitTime\"}],\"errorType\":\"skip\",\"isDebug\":false,\"timeOut\":\"30\",\"contentType\":\"phone\"},\"desc\":\"A TikTok Task flow\",\"title\":\"TikTok\"}"
	}
}
```

## Error Codes

For error codes, please refer to [Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 48002 | custom task flow not found |

---

#### Cloud Phone API / Automation / Other Task

##### Multichannel video distribution

[TOC]

API Description
---------------

* TikTok/Instagram Reels/YouTube Shorts Video Distribution

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/multiPlatformVideoDistribution`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| title | Yes | string | Title, up to 100 characters |
| video | Yes | \[\]string | Videos, up to 10 videos, refer to the User Guide - File Upload for creating automation tasks |

Request Example
----------------

```json
{
  "name":"test",
  "remark":"test remark",
  "scheduleAt": 1741846843,
  "id":"557536075321468390",
  "title":"title",
  "video": ["https://singapore-upgrade.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Upload files to the cloud machine in batches

[TOC]


Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/fileUpload`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| files | Yes | \[\]string | Files, up to 100, refer to the User Guide - File Upload for creating automation tasks |

Request Example
----------------

```json
{
	"name":"test",
	"remark":"test remark",
	"scheduleAt": 1741846843,
	"id":"557536075321468390",
	"files": ["https://material.geelark.com/a.mp4"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Batch import contacts to cloud phone

[TOC]


Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/importContacts`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| contacts | Yes | array[ContactParam] | Array of contact information |

### Contact Information - ContactParam

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
|email1|No|string|Email 1|
|email2|No|string|Email 2|
|fax|No|string|Fax number. At least one of the mobile phone number, work mobile phone number and fax number must be non-empty|
|firstName|No|string|First name. At least one of the first name and last name must be non-empty|
|lastName|No|string|Last name. At least one of the first name and last name must be non-empty|
|mobile|No|string|Mobile phone number. At least one of the mobile phone number, work mobile phone number and fax number must be non-empty|
|work|No|string|Work mobile phone number. At least one of the mobile phone number, work mobile phone number and fax number must be non-empty|

Request Example
----------------

```json
{
	"name":"test",
	"remark":"test remark",
	"scheduleAt": 1741846843,
	"id":"557536075321468390",
	"contacts": [
		{
			"firstName": "jay",
			"mobile": "13288888888"
		}
	]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Upload Keybox to the cloud phone

[TOC]

Request URL
-----------

* `https://openapi.geelark.com/open/v1/rpa/task/keyboxUpload`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| name | No | string | Task name, up to 128 characters |
| remark | No | string | Remarks, up to 200 characters |
| scheduleAt | Yes | integer | Scheduled time (timestamp) |
| id | Yes | string | Cloud phone ID |
| files | Yes | \[\]string | Files, up to 100, refer to the User Guide - File Upload for creating automation tasks |

Request Example
----------------

```json
{
	"name":"test",
	"remark":"test remark",
	"scheduleAt": 1741846843,
	"id":"557536075321468390",
	"files": ["https://material.geelark.com/a.xml"]
}
```

Response Example
----------------

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

### Cloud Phone API / Shell

#### Execute shell command

[TOC]

## Interface Description
Execute shell commands on cloud phones.

- Only supports `Android10`/ `Android12`/`Andriod13`/`Andriod14`/`Andriod15` models.

## Request URL

- `https://openapi.geelark.com/open/v1/shell/execute`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| -------------- | -------- | ------ | --------------------- | ----------------- |
| id | Yes | string | Cloud phone ID | Refer to Request Example |
| cmd | Yes | string | Command to execute | Refer to Request Example |

## Request Example
```json
{
 "id": "528715748189668352",
 "cmd": "pm list packages"
}
```

## Response Example

```json
{
 "traceId": "924A8E4AAC9E0B0B96ABA7B8801B2CBE",
 "code": 0,
 "msg": "success",
 "data": {
 "status": true,
		"output": "com.zhiliaoapp.musically"
 }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| -------------- | ------ | ------------------------------------ |
| status | bool | true: Execution successful, false: Execution failed |
| output | string | Execution result |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| ---------- | ---------------------------------- |
| 42001 | Cloud phone does not exist |
| 42002 | Cloud phone is not in running state |
| 50001 | Cloud phone does not support shell commands |

---

### Cloud Phone API / Application Management

#### Get installed applications

[TOC]

API Description
---------------

Retrieve the list of applications installed on the cloud phone.

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/app/list`

Request Method
--------------

*   POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envId | Yes | string | Cloud phone environment ID | 123456654321 |
| page | Yes | integer | Page number, minimum is 1 | 1 |
| pageSize | Yes | integer | Number of items per page, minimum is 1, maximum is 100 | 10 |

Request Example
---------------

```json
{
    "envId" : "1809135651036667904",
    "page" : 1,
    "pageSize" : 5
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of items |
| page | integer | Page number |
| pageSize | integer | Page size |
| items | array\[AppInfo\] | Array of application data |

### AppInfo

| Parameter Name | Type | Description |
| --- | --- | --- |
| appIcon | string | Application icon URL |
| appId | string | Application ID |
| appName | string | Application name |
| appVersionId | string | Application version ID |
| installStatus | integer | Installation status: 0-Installing, 1-Installed, 2-Failed, 3-Uninstalling, 4-Uninstalled, 5-Uninstall Failed, others-Not Installed |
| installTime | string | Installation time |
| packageName | string | Application package name |
| versionCode | string | Application version code |
| versionName | string | Application version name |

Response Example
----------------

```json
{
    "traceId": "123",
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "appIcon": "http://cmp1-prod.zxpcloud.com/apps/io.tm.k.drama/K-DRAMA_1716451323126.png",
                "appId": "1793552962123993090",
                "appName": "K-DRAMA",
                "appVersionId": "1793552962140770305",
                "installStatus": 1,
                "installTime": "2024-07-10 23:07:56",
                "packageName": "io.tm.k.drama",
                "versionCode": "21120300",
                "versionName": "1.0.1"
            }
        ],
        "total": 1,
        "page": 1,
        "pageSize": 5
    }
}
```

Error Codes
-----------

The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The corresponding cloud phone does not exist |

---

#### Get available applications

[TOC]

## API Description

Get the list of apps available for installation on the cloud phone.

## Request URL

*   `https://openapi.geelark.com/open/v1/app/installable/list`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| name | No | string | Search keyword | tiktok |
| envId | Yes | string | Cloud phone environment ID | 123456654321 |
| getUploadApp | No | bool | get upload app | true |
| page | Yes | integer | Page number, minimum is 1 | 1 |
| pageSize | Yes | integer | Number of items per page, minimum is 1, maximum is 100 | 10 |

## Request Example

```json
{
    "name" : "tiktok",
    "envId" : "1809135651036667904",
	"getUploadApp" : false,
    "page" : 1,
    "pageSize" : 5
}
```

## Response Body Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of tasks |
| page | integer | Page number |
| pageSize | integer | Page size |
| items | array\[AmpAppInfo\] | List of data items |

### Installable App Information `AmpAppInfo`

| Parameter Name | Type | Description |
| --- | --- | --- |
| appIcon | string | App icon URL |
| id | string | App ID |
| appName | string | App name |
| packageName | string | App package name |
| appVersionInfoList | array\[AmpAppVersionInfo\] | List of app versions |

### Installable App Version Information `AmpAppVersionInfo`

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | App version ID |
| installStatus | integer | Installation status: 0 - Installing, 1 - Installed, 2 - Installation Failed, 3 - Uninstalling, 4 - Uninstalled, 5 - Uninstallation Failed, others - Not Installed |
| versionCode | string | App version code |
| versionName | string | App version name |

## Response Example


```json
{
    "traceId": "123",
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "appIcon": "http://cmp1-prod.zxpcloud.com/apps/io.tm.k.drama/K-DRAMA_1716451323126.png",
                "appName": "K-DRAMA",
                "appVersionInfoList": [
                    {
                        "id": "1793552962140770305",
                        "installStatus": 1,
                        "versionCode": 21120300,
                        "versionName": "1.0.1"
                    }
                ],
                "id": "1793552962123993090",
                "installStatus": 1,
                "packageName": "io.tm.k.drama"
            }
        ],
        "total": 1,
        "page": 1,
        "pageSize": 5
    }
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The specified cloud phone does not exist |

---

#### Install application

[TOC]

## API Description

Install an app.

## Request URL

*   `https://openapi.geelark.com/open/v1/app/install`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envId | Yes | string | Cloud phone environment ID | 1809135651036667904 |
| appVersionId | Yes | string | App version ID | 1793552962140770305 |

## Request Example
```json
{
    "envId" : "1809135651036667904",
    "appVersionId" : "1793552962140770305"
}
```

## Response Example

```json
{
    "traceId": "123",
    "code": 0,
    "msg": "success"
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The specified cloud phone does not exist |
| 42002 | The cloud phone is not in running state |
| 42003 | The app is currently being installed |
| 42004 | A higher version of the app is already installed, installing a lower version is not allowed |
| 42006 | app not exist |

---

#### Start application

[TOC]

## API Description

Start an app.

## Request URL

*   `https://openapi.geelark.com/open/v1/app/start`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envId | Yes | string | Cloud phone environment ID | 1809135651036667904 |
| appVersionId | No | string |App version ID (either appVersionId or packageName must be provided) | 1793552962140770305 |  
| packageName | No | string | Application package name (either appVersionId or packageName must be provided)| com.zhiliaoapp.musically |

## Request Example

```json
{
    "envId" : "1809135651036667904",
    "appVersionId" : "1793552962140770305"
}
```

## Response Example

```json
{
    "traceId": "123",
    "code": 0,
    "msg": "success"
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The specified cloud phone does not exist |
| 42002 | The cloud phone is not in a running state |
| 42005 | The corresponding app is not installed |
| 42003 | App is installing |

---

#### Stop application

[TOC]

## API Description

Close an app.

## Request URL

*   `https://openapi.geelark.com/open/v1/app/stop`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envId | Yes | string | Cloud phone environment ID | 1809135651036667904 |
| appVersionId | No | string |App version ID (either appVersionId or packageName must be provided) | 1793552962140770305 |  
| packageName | No | string | Application package name (either appVersionId or packageName must be provided)| com.zhiliaoapp.musically |

## Request Example

```json
{
    "envId" : "1809135651036667904",
    "appVersionId" : "1793552962140770305"
}
```

## Response Example

```json
{
    "traceId": "123",
    "code": 0,
    "msg": "success"
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The specified cloud phone does not exist |
| 42002 | The cloud phone is not in a running state |
| 42005 | The corresponding app is not installed |

---

#### Uninstall application

[TOC]

## API Description

Uninstall an app.

## Request URL

* `https://openapi.geelark.com/open/v1/app/uninstall`

## Request Method

* POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envId | Yes | string | Cloud phone environment ID | 1809135651036667904 |
| packageName | Yes | string | Application package name| com.zhiliaoapp.musically |
~~| appVersionId | No | string |App version ID (either appVersionId or packageName must be provided) | 1793552962140770305 |~~

## Request Example

```json
{
 "envId" : "1809135651036667904",
 "packageName" : "com.zhiliaoapp.musically"
}
```

## Response Example

```json
{
 "traceId": "123",
 "code": 0,
 "msg": "success"
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | The specified cloud phone does not exist |
| 42002 | The cloud phone is not in a running state |
| 42005 | The corresponding app is not installed |

---

#### Upload Application

[TOC]

## API Description

Upload Application

## Request URL

- `https://openapi.geelark.com/open/v1/app/upload`

## Request Method

- POST

## Request Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| fileUrl | Yes | string | Application installation file link (supports apk, xapk only) | https://material.geelark.cn/user-upload/495622401615203830/apk/uCeztwvXpswsHPH5WFht.apk |
| desc | No | string | Remarks | Application description |

## Request Example

```json
{
    "fileUrl" : "https://material.geelark.cn/user-upload/495622401615203830/apk/uCeztwvXpswsHPH5WFht.apk",
    "desc" : "app description"
}
```

## Response Data Description

| Parameter | Type | Description |
| --- | --- | --- |
| taskId | string | Task ID for querying upload status |

## Response Example

```json
{
    "traceId": "B82825D58F85FB31B755BD6CA32A30A9",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "1830906144634757120"
    }
}
```

## Error Codes

Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Query Application Upload Status

[TOC]

##  API Description

Query Application Upload Status

## Request URL

- `https://openapi.geelark.com/open/v1/app/upload/status`

## Request Method

- POST

## Request Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string | Task ID | 1830906144634757120 |

## Request Example

```json
{
    "taskId" :  "1830906144634757120"
}
```

## Response Data Description

| Parameter | Type | Description |
| --- | --- | --- |
| status | integer | Status (0: in the process of being uploaded; 1: uploaded successfully; 2: upload failed; 3: not approved in review) |
| appName | string | Application name |
| appIcon | string | Application icon |
| appId | string | Application ID |
| versionId | string | Application version ID |

## Response Example

```json
{
    "traceId": "B9C9A787A1B559A6B883A171A7EA129B",
    "code": 0,
    "msg": "success",
    "data": {
        "status": 1,
        "appName": "パワサカ",
        "appIcon": "https://material.geelark.cn/app/icon/20240903/223wgZeZq3.jpg",
        "appId": "1813124121385549826",
        "versionId": "1813124121435881473"
    }
}
```

## Error Codes

The following are specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42007 | Task does not exist |

---

#### Get the application list

[TOC]

## API Description

Get the application list

## Request URL

- `https://openapi.geelark.com/open/v1/app/shop/list`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| key | No | string | Search keyword | tiktok |
| getUploadApp | No | bool | Get uploaded apps | true |
| page | Yes | integer | Page number, minimum is 1 | 1|
| pageSize | Yes | integer | Number of data items per page, minimum is 1, maximum is 200 | 10|

## Request Example

```json
{
    "key" : "tiktok",
	"getUploadApp" : false,
    "page" : 1,
    "pageSize" : 5
}
```

## Response Example

```json
{
	"traceId":"123",
	"code":0,
	"msg":"success",
	"data":{
		"items":[
			{
				"appIcon":"http://cmp1-prod.zxpcloud.com/apps/io.tm.k.drama/K-DRAMA_1716451323126.png",
				"appName":"K-DRAMA",
				"appVersionList":[
					{
						"id":"1793552962140770305",
						"versionCode":21120300,
						"versionName":"1.0.1"
					}
				],
				"id":"1793552962123993090"
			}
		],
		"total":1,
		"page":1,
		"pageSize":5
	}
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| total | integer   | Total number  |
| page | integer   | Page number  |
| pageSize | integer   | Page size  |
| items | array[AmpAppInfo]   | Data array  |

### Application Information AmpAppInfo

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| appIcon | string | Application icon |
| id | string | Application id |
| appName | string | Application name |
| appVersionList | array[AmpAppVersionInfo] | Application version information |

### Application version information AmpAppVersionInfo

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| id | string | Application version id |
| versionCode | integer | Application version code |
| versionName | string | Application version name |

## Error Codes

Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Add to Team Applications

[TOC]

## API Description

Add the app to the team Applications and it will be automatically installed after the cloud phone is started

## Request URL

- `https://openapi.geelark.com/open/v1/app/add`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | yes | string | Application id; Please call the “Get Application List” API to obtain it. | 1793552962123993090 |
| versionId | yes | string | Version id; Please call the “Get Application List” API to obtain it. | 1793552962140770305 |
| installGroupIds | no | array[string] | Environment groups allowed for installation. Defaults to all environment groups. "0" indicates no grouping;Please call the query group API first to obtain the group ID. | ["528715748189668352"] |

## Request Example

```json
{
 "id": "1793552962123993090",
 "versionId": "1793552962140770305",
 "installGroupIds": ["0"]
}
```

## Response Example

```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes

Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Get Team App List

[TOC]

## API Description

Get Team Application List

## Request URL


- `https://openapi.geelark.com/open/v1/app/teamApp/list`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | Yes | Integer | Page number, minimum is 1 | 1|
| pageSize | Yes | Integer | Number of records per page, minimum is 1, maximum is 200 | 10|


## Request Example


```json
{
 "page" : 1,
 "pageSize" : 5
}
```


## Response Example


```json
{
	"traceId":"97CBBCCB8DAFC8D1BDEFB943945BFC95",
	"code":0,
	"msg":"success",
	"data":{
		"total":4,
		"page":1,
		"pageSize":1,
		"items":[
			{
				"id":"497652752864775437",
				"appName":"TikTok",
				"appIcon":"https://material.geelark.cn/app/icon/20251026/kVAQ8OuTNF.png",
				"versionId":"1793552962123993090",
				"versionCode":410903,
				"versionName":"41.9.3",
				"status":0,
				"isUpload":false,
				"uploadStatus":0,
				"appAuth":0,
				"appRoot":0,
				"envGroups":[]
			}
		]
	}
}
```


## Response Data Description


| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| total | integer | Total number |
| page | integer | Page number |
| pageSize | integer | Page size |
| items | array[AppTeamAppListItem] | Data array |

### Application Information AppTeamAppListItem

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| id | string | Team application ID |
| appName | string | Application name |
| appIcon | string | Application icon |
| versionId | string | Version ID |
| versionCode | integer | Version number |
| versionName | string | Version name |
| status | integer | Whether to install automatically, 0 for no, 1 for yes |
| isUpload | bool | Application being uploaded |
| uploadStatus | integer | Upload status, 0 for uploading, 1 for successful upload, 2 for failed upload, 3 for failed review |
| appAuth | integer | App authorization, 0 for off authorization, 1 for on authorization |
| appRoot | integer | App root, 0 for off, 1 for on |
| envGroups | array[string] | Allowed environment group IDs, empty represents all environment groups, 0 represents no group |

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Remove Team Apps

[TOC]

## API Description

Remove the application from the team applications.

## Request URL


- `https://openapi.geelark.com/open/v1/app/remove`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |


## Request Example


```json
{
 "id": "497652752864775437"
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Set Team Apps to Install Automatically

[TOC]

## API Description

Set up automatic installation for team applications. Once automatic installation is enabled, the applications will be installed after the cloud phone starts up.

## Request URL


- `https://openapi.geelark.com/open/v1/app/setStatus`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |
| status | Yes | integer | Whether to install automatically, 0 for no, 1 for yes | 1 |
| installGroupIds | No | array[string] | Allowed environment groups for installation, defaults to all environment groups, 0 represents no group | ["497652752864775437"] |

## Request Example


```json
{
 "id": "497652752864775437",
 "status": 1
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Set Team App Authorization

[TOC]

## API Description

Grant team application permissions, including all permissions such as location permissions, which only apply to newly installed applications.

## Request URL


- `https://openapi.geelark.com/open/v1/app/auth/status`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |
| appAuth | Yes | integer | App authorization 0 disables authorization; 1 enables authorization | 1 |


## Request Example


```json
{
 "id": "497652752864775437",
 "appAuth": 1
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Set Team App ROOT Access

[TOC]

## API Description

Enable or disable team application ROOT

## Request URL


- `https://openapi.geelark.com/open/v1/app/root`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |
| opera | Yes | integer | Operation, 0 off, 1 on | 1 |


## Request Example


```json
{
 "id": "497652752864775437",
 "opera": 1
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Batch Operate Cloud Phone App

[TOC]

## API Description

Batch operation of applications on opened cloud phone

## Request URL


- `https://openapi.geelark.com/open/v1/app/operation/batch`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| action | Yes | interger | Operation type 1 Startup; 2. Close; 3. Restart; 4 Installation; 5 Uninstalling | 1 |
| groupIds | No | array[string] | Group ID, operate on the opened cloud phone under the specified group, default to all | ["595681312937911830"] |
| packageName | No | string | Application package name, startup/close/restart/uninstall, choose between packageName/versionId , recommended to use package name | io.tm.k.drama |
| versionId | No| string | Application version ID, required for installation, can be obtained through the/app/teamApp/list interface |1793552962140770305 |


### Request Example


Startup
```json
{
    "action" : 1,
    "groupIds" : ["595681312937911830"],
    "packageName": "io.tm.k.drama"
}
```

Installation
```json
{
    "action" : 1,
    "groupIds" : ["595681312937911830"],
    "versionId": "1793552962140770305"
}
```

## Response Data Description

### items 
| Parameter Name | Type | Description |
| --- | --- | --- |
| id | integer   | cloud phone id  |
| errCode | integer   | Error code 1: The application is currently being installed/uninstalled; 2 corresponding apps not installed  |

### Response Example


```json
{
    "traceId": "A0598A2CA0802A98957B9E1F87EB9289",
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "id": "583502967211075086",
                "errCode": 2
            }
        ]
    }
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Set Team App Keep Alive

[TOC]

## API Description

Enable or disable team app keep-alive. Only available for the Pro Plan.
Only Android 12/13/14/15 are supported. One app can be kept alive at max.
On Android 12/13/15, if the app is already running before keep-alive is enabled, please restart the App to take effect.
On Android 14, it will take effect immediately, without the need to restart the App or the cloud phone.

## Request URL


- `https://openapi.geelark.com/open/v1/app/setKeepAlive`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |
| opera | Yes | integer | Operation, 0 off, 1 on | 1 |


## Request Example


```json
{
 "id": "497652752864775437",
 "opera": 1
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 44001 | Please upgrade to the Pro plan |

---

#### Set Team App Auto Start

[TOC]

## API Description

Enable or disable team application auto-start

## Request URL


- `https://openapi.geelark.com/open/v1/app/setAutoStart`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Team application ID | 497652752864775437 |
| opera | Yes | integer | Operation, 0 off, 1 on | 1 |


## Request Example


```json
{
 "id": "497652752864775437",
 "opera": 1
}
```


## Response Example


```json
{
 "traceId": "886A92FCBE9B7A52A7F583FCBD2BF6A8",
 "code": 0,
 "msg": "success"
}
```

## Error Codes


Please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Cloud Phone API / ADB

#### Set ADB Status

[TOC]

API Description
---------------
* Currently, ADB only supports Android 9,11,12,13 ,14, 15,16 devices.
* Before set ADB status. Please start the cloud phone first.
* Enabling ADB is an asynchronous operation. It is recommended to wait about 3 seconds after enabling ADB before retrieving port, password, and other information.

Request URL
-----------

* `https://openapi.geelark.com/open/v1/adb/setStatus`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | Array of cloud phone environment IDs, maximum 200| Refer to request example |
| open | Yes | bool | Open/Close | false |

## Request Example

```json
{
 	"ids" : [
		 "526209711930868736"
	 ],
 	"open" : true
}
```


## Response Example

```json
{
 "traceId": "A24A3089958A4BC28E8B89B3AE1A61AC",
 "code": 0,
 "msg": "success"
}
```

Error Codes
-----------

For error codes, please refer to  [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

#### Get ADB information

[TOC]

API Description
---------------

Retrieve ADB Information

Request URL
-----------

* `https://openapi.geelark.com/open/v1/adb/getData`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array\[string\] | Array of cloud phone IDs, maximum 200 | \["526209711930868736"\] |

Request Example
---------------

```json
{
 "ids" : ["526806961778328576","524798337208026112","524783756767134720"]
}
```


Response Data Description
-------------------------
### items
| Parameter Name | Type | Description |
| --- | --- | --- |
| code | integer | Error code: 0 indicates success; for other codes, refer to the error code table |
| id | string | Cloud phone ID |
| ip | string | Connection IP |
| port | string | Port |
| pwd | string | The password for glogin |

Response Example
----------------

```json
{
    "traceId": "8AB9D6B482B679ECB5578314903B80B9",
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "code": 0,
                "id": "524783756767134720",
                "ip": "124.71.210.176",
                "pwd": "8c1da4",
                "port": "25219"
            },
            {
                "code": 42002,
                "id": "524798337208026112",
                "ip": "",
                "pwd": "",
                "port": ""
            }
        ]
    }
}
```

Error Codes
-----------

The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 42002 | Cloud phone is not running |
| 49001 | ADB is not enabled |
| 49002 | The device does not support ADB |

---

#### Common ADB Commands

[TOC]


Common Commands
---------------

GeeLark Cloud Phone supports all Android **adb** commands. Below are some frequently used commands.  
To enable adb, please refer to: [https://help.geelark.com/adb](https://help.geelark.com/adb)

### Connect adb
For Windows users, open Command Prompt, or for macOS users, open Terminal. Type "adb connect *IP address for connection*" to connect to your desired IP address.
Next, enter the login command with your connection code: adb -s *IP address for connection* shell glogin f850ef
```shell
adb connect 124.71.210.176:21781
adb shell glogin f850ef
```


### Upload a file from your local computer to the cloud phone

```shell
adb push /Users/geelark/Downloads/movie.mp4 /sdcard/movie.mp4
```

### Download a file from the cloud phone to your local computer
```shell
adb pull /sdcard/movie.mp4 /Users/geelark/Downloads/movie.mp4 
```

### Get cloud phone device ID
```shell
//Android 13：Version
adb shell getprop ro.boot.serialno
//other Android version：
adb shell getprop ro.serialno

```

### Get cloud phone environment ID
```shell
adb shell getprop ro.gl.serialno
```

### Capture the cloud phone screen and save it locally
```shell
adb exec-out screencap -p > /Users/geelark/Downloads/screenshot.png
```

### Record the cloud phone screen and save it locally
```shell
adb shell screenrecord /sdcard/demo.mp4
adb pull /sdcard/demo.mp4 /Users/geelark/Downloads/demo.mp4
```

### Install an app to the cloud phone
```shell
//（-r:recover，-g:grant permission）
adb install -r -g /Users/geelark/Downloads/tiktok.apk
```

### Uninstall an app
```shell
adb uninstall com.ss.android.ugc.aweme
```

### Tap on coordinates
```shell
// click(400,360)
adb shell input tap 400 360
// long lick(400,360)
adb shell input swipe 400 360 400 360 1000
// swipe from(400,1200)to(400,100)
adb shell input swipe 400 1200 400 100 1000
```

---

### Cloud Phone API / File Management

#### Upload temporary files to GeeLark

[TOC]

#1. Obtain a temporary upload URL "uploadUrl" for the file.

API Description
---------------

Upload temporary files to GeeLark (Expires in 3 days),if need to save for a longer time, please upload it to the [Library](https://open.geelark.com/api/get-material-upload-url "Library").

Request URL
-----------

* `https://openapi.geelark.com/open/v1/upload/getUrl`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| fileType | Yes | string | File type, Currently supported: "jpg", "jpeg", "png", "gif", "bmp", "webp","heif", "heic", "mp4", "webm","xml", "apk", "xapk" |"mp4"|

Request Example
---------------


```json
{
    "fileType": "mp4"
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| uploadUrl | string | URL for uploading the file (valid for 30 minutes) |
| resourceUrl | string | URL to access the resource |

Response Example
----------------

```json
{
 "traceId": "9F49062C8DB3C90D8E94B4DFA37BDF89",
 "code": 0,
 "msg": "success",
 "data": {
 "uploadUrl": "http://42-studio-prod.oss-cn-hangzhou.aliyuncs.com/open-upload%2F497521349346987872%2F20240730%2Fe2u5amyB.mp4?Expires=1722310832&OSSAccessKeyId=REDACTED_OSS_KEY&Signature=HGBVqTUfXcUAthLPnO3ZYIVnAxg%3D",
 "resourceUrl": "https://material-prod.geelark.cn/open-upload/497521349346987872/20240730/e2u5amyB.mp4"
 }
}
```

Error Codes
-----------

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

# 2.Upload the file using "uploadUrl" (after a successful upload, the file can be accessed via resourceUrl).

Upload Usage Example
-----------

### linux
``` shell
curl -X PUT --upload-file ./upload_test.mp4 "uploadUrl"
```

### Go
```go
// upload file path
filePath := "/Users/xxx/Desktop/upload_test.mp4"

// open file
file, err := os.Open(filePath)
if err != nil {
 fmt.Println("Error opening file:", err)
 return
}

// create http client
url := "uploadUrl"
req, err := http.NewRequest("PUT", url, file)
if err != nil {
 fmt.Println("Error creating request:", err)
 return
}

// send request
client := &http.Client{}
resp, err := client.Do(req)
if err != nil {
 fmt.Println("Error sending request:", err)
 return
}
defer resp.Body.Close()

// handle response
if resp.StatusCode == http.StatusOK {
 fmt.Println("File uploaded successfully!")
} else {
 fmt.Println("Error uploading file:", resp.Status)
}
```
## Postman
Please note that the header cannot pass any extra fields!
![](http://doc.geelark.cn/server/index.php?s=/api/attachment/visitFile&sign=55a9c6fd741b6c9b78e71e4beb948dd3)
![](http://doc.geelark.cn/server/index.php?s=/api/attachment/visitFile&sign=e9ccd1ef2db200455f61ce465a989b20)

---

#### Upload files to the cloud phone

[TOC]

API Description
---------------

Upload files to the cloud phone.  
Before uploading, please start the cloud phone. The file will be uploaded to the "Downloads" folder of the cloud phone.

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/uploadFile`

Request Method
--------------

*   POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Cloud phone ID | Refer to request example |
| fileUrl | Yes | string | File URL | Refer to request example |

Request Example
---------------
```json
{
    "id": "528715748189668352",
	"fileUrl" : "https://material-prod.geelark.cn/app/icon/20240506/nFrUEcRc9I.jpg"
}
```

Response Example
----------------

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "taskId": "1850726441252569088"
    }
}
```
Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| taskId | string | Task ID |

Error Codes
-----------

The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 42002 | Cloud phone is not running |

Callback Result and Example
---------------------------

Please refer to Callback Example

---

#### Query the upload status of files to the cloud phone

[TOC]

API Description
---------------

Query the upload status of files to the cloud phone.  
You can actively retrieve the result within one hour of initiating the upload task; after expiration, the retrieval will fail.

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/uploadFile/result`

Request Method
--------------

*   POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string | Task ID | Refer to request example |

Request Example
---------------
```json
{
    "taskId": "528715748189668352"
}
```

Response Example
----------------


```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "status": 1
    }
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| status | integer | 0: Failed to retrieve; 1: Uploading; 2: Upload successful; 3: Upload failed |

Error Codes
-----------

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Upload the keybox file

[TOC]

API Description
---------------

Upload the keybox file and pass Google's integrity verification. This is currently only supported on Android 12/13/15. For Android 12/13, simply upload the keybox file. Android 15 requires the following additional steps:
1. Update Google Play and GMS to the latest version.
2. Log in with a valid Google account.
3. Download the Play Integrity API Checker from Google Play.

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/keyboxUpload`

Request Method
--------------

*   POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Cloud phone ID | Refer to request example |
| fileUrl | Yes | string | File URL | Refer to request example |

Request Example
---------------
```json
{
    "id": "528715748189668352",
	"fileUrl":"https://material.geelark.cn/client-img/oakendn.xml"
}
```

Response Example
----------------

```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "taskId": "1850726441252569088"
    }
}
```
Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| taskId | string | Task ID |

Error Codes
-----------

The following are specific error codes for this API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 42001 | Cloud phone does not exist |
| 42002 | Cloud phone is not running |
| 43026  | Cloud phone system not support             |
| 60003  | Invalid file url                |

Callback Result and Example
---------------------------

Please refer to Callback Example

---

#### Query the upload keybox file task result

[TOC]

API Description
---------------

After calling the upload Keybox file interface, get the execution result through the returned taskId

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/phone/keyboxUpload/result`

Request Method
--------------

*   POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string | Task ID | Refer to request example |

Request Example
---------------
```json
{
    "taskId": "528715748189668352"
}
```

Response Example
----------------


```json
{
    "traceId": "A62BBBF3A294487F9B49B9FFA0F84CA8",
    "code": 0,
    "msg": "success",
	"data": {
        "status": 1
    }
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| status | integer |  0: Uploading; 1: Upload successful; 2: Upload failed |

Error Codes
-----------

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Cloud Phone API / Library

#### Upload files to the Library

[TOC]

#1. Get the Upload URL for Uploading a File to the Library

API Description
---------------

Upload a file to the Library, the file is valid for 30 days. Please add it to the Library immediately after successful upload, if the file not added, it will be deleted.

Request URL
-----------

- `https://openapi.geelark.com/open/v1/material/getUploadUrl`

Request Method
--------------

* POST

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| fileType | Yes | string | File type, Currently supported: "jpg", "jpeg", "png", "gif", "bmp", "webp","heif", "heic", "mp4", "webm","xml", "apk", "xapk" | "jpg" |

Request Example
---------------


```json
{
    "fileType": "jpg"
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| uploadUrl | string | URL for uploading the file (valid for 30 minutes) |
| resourceUrl | string | URL to access the resource |

Response Example
----------------

```json
{
    "traceId": "AC5B5C9ABF8BF925A504A8849A4862B2",
    "code": 0,
    "msg": "success",
    "data": {
        "uploadUrl": "http://42-studio-singapore.oss-ap-southeast-3.aliyuncs.com/open-material-upload%2F503609206784396150%2F20260309%2FVwujVZdl.jpg?Expires=1773046044&OSSAccessKeyId=REDACTED_OSS_KEY&Signature=TZbYGwfcad4XFiyh4mZ1gdVI%2FzI%3D",
        "resourceUrl": "https://singapore-upgrade.geelark.com/open-material-upload/503609206784396150/20260309/VwujVZdl.jpg"
    }
}
```

Error Codes
-----------

For error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

# 2.Upload the file using "uploadUrl" (after a successful upload, the file can be accessed via resourceUrl).

Upload Usage Example
-----------

### linux
``` shell
curl -X PUT --upload-file ./upload_test.jpg "uploadUrl"
```

### Go
```go
// upload file path
filePath := "/Users/xxx/Desktop/upload_test.mp4"

// open file
file, err := os.Open(filePath)
if err != nil {
 fmt.Println("Error opening file:", err)
 return
}

// create http client
url := "uploadUrl"
req, err := http.NewRequest("PUT", url, file)
if err != nil {
 fmt.Println("Error creating request:", err)
 return
}

// send request
client := &http.Client{}
resp, err := client.Do(req)
if err != nil {
 fmt.Println("Error sending request:", err)
 return
}
defer resp.Body.Close()

// handle response
if resp.StatusCode == http.StatusOK {
 fmt.Println("File uploaded successfully!")
} else {
 fmt.Println("Error uploading file:", resp.Status)
}
```
## Postman
Please note that the header cannot pass any extra fields!
![](http://doc.geelark.com/server/index.php?s=/api/attachment/visitFile&sign=cce0a71903f159b1db961d12744344e7)
![](http://doc.geelark.com/server/index.php?s=/api/attachment/visitFile&sign=ae5829e137fe8c2860471990237fc020)

---

#### Create material

[TOC]

## Interface Description
create material

## Request URL

- `https://openapi.geelark.com/open/v1/material/create`

## Request Method


- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| url | Yes | string | please refer to [Upload a file to the Library](https://open.geelark.com/api/get-material-upload-url)   | Refer to Request Example |
| tagsId | No | array[string] | tags id | Refer to Request Example |
| fileName | No | string | file name, up to 200 characters  | Refer to Request Example |


## Request Example
```json
{
 "url" : "https://material.geelark.cn/client-img/banner0903_cn.gif",
 "tagsId" : ["569577509402731994","569577514586891738"],
 "fileName": "a.jpg"
}
```


## Response Example

```json
{
 "traceId": "ADD9A7489BB2198DBC0FB37082684CB0",
 "code": 0,
 "msg": "success",
 "data": {
 "id": "570606523940605924",
 "failDetails": [
 {
 "id": "5695775094027319941",
 "code": 43022,
 "msg": "tag not found"
 }
 ]
 }
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| id | string | material id |
| failDetails | array[FailDetails] | Failure details |

### Failure Details <FailDetails>

| Parameter Name | Type | Description |
| ------------ | ---------- | ------------ |
| code | integer | Error code |
| id | string | Tag ID |
| msg | string | Error msg |

## Error Codes

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 60001 | the material library has reached its maximum capacity |
| 60003 | illegal url，please upload temporary files to GeeLark and get the url |
| 60004 | The file format is not supported |
| 43022  | tag not found |
| 40005  | The resource does not exist. Please check if the URL resource is available |

---

#### Delete material

[TOC]

## Interface Description
delete material

## Request URL

- `https://openapi.geelark.com/open/v1/material/del`

## Request Method


- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array[string] | material id |Refer to Request Example   |

## Request Example
```json
{
    "ids" : ["569569510948864567"]
}
```


## Response Example

```json
{
    "traceId": "A1A84FBC88912B5A9F77B681B2A9A983",
    "code": 0,
    "msg": "success",
    "data": {
        "totalAmount": 1,
        "successAmount": 0,
        "failAmount": 1,
        "failDetails": [
            {
                "id": "5695695109488645671",
                "code": 60005,
                "msg": "material not found"
            }
        ]
    }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| -------------- | ----------------- | -------------------- |
| totalAmount    | integer           | Total delete requests |
| successAmount  | integer           | Total successes      |
| failAmount     | integer           | Total failures       |
| failDetails    | array[FailDetails] | Failure details      |

### Failure Details <FailDetails>

| Parameter Name | Type              | Description          |
| ------------ | ---------- | ------------ |
| code           | integer | Error code  |
| id             | string  | Tag ID     |
| msg            | string  | Error msg   |

## Error Codes

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 60005  | material not found |

---

#### Set material tag

[TOC]

## Interface Description
set material tag

## Request URL

- `https://openapi.geelark.com/open/v1/material/tag/set`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description           | Example           |
| --- | --- | --- | --- | --- |
| materialsId | Yes | array[string] | material id | Refer to Request Example  |
| tagsId | No | array[string] | tags id，Each tagging operation will delete all existing tags and only retain the newly set tags | Refer to Request Example  |


## Request Example
```json
{
 "materialsId" : ["570457374221926935"],
 "tagsId" : ["570461738663674391"]
}
```


## Response Example

```json
{
    "traceId": "AC3ADD84BEA1D8D2A7DDAF8B90A8D2A8",
    "code": 0,
    "msg": "success",
    "data": {
        "failDetails": [
            {
                "id": "5704573742219269351",
                "code": 60005,
                "msg": "material not found"
            },
            {
                "id": "5704617386636743911",
                "code": 43022,
                "msg": "tag not found"
            }
        ]
    }
}
```

## Response Data Description
### failDetails Failure Info <FailDetails>


| Parameter Name | Type    | Description |
| -------------- | ------- | ----------- |
| code           | integer | Error code  |
| id             | string  | Tag ID      |
| msg            | string  | Error msg   |


## Error Codes

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43022  | tag not found |
| 60005  | material not found |

---

#### Search material

[TOC]


## Interface Description
search material



## Request URL


- `https://openapi.geelark.com/open/v1/material/search`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type          | Description           | Example           |
| --- | --- | --- | --- | --- |
| page | No | integer | page | Refer to Request Example  |
| pageSize | No | integer | page size （max: 200） | Refer to Request Example  |
| fileName | No | string | search file name | Refer to Request Example  |
| tagsId | No | array[string] |search tag id | Refer to Request Example  |
| source | No | integer | source: 0-upload，1-AI Edit 2Baidu  Cloud Drive 3GhostCut 4GoogleDrive 5Image to video | Refer to Request Example  |
| fileType | No | array[integer] | file type  1-image，2-video | Refer to Request Example  |
| ids | No | array[string] |ID array，The maximum length of the array is 100. | ["5213214343124321"] |



## Request Example
```json
{
    "fileType" : [1],
    "fileName" : "demo",
    "tagIds" : ["569577514586891738"],
    "source" : 1,
    "page" : 1,
    "pageSize" : 50,
    "ids": ["608127302118696420"] 
}
```



## Response Example


```json
{
    "traceId": "8D192F0785AEAAFA879FA44A990BEDAC",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 12,
        "page": 1,
        "pageSize": 50,
        "list": [
            {
                "id": "569546671000653787",
                "createdTime": 1749005870,
                "fileName": "2025_06_02_11_31_IMG_9607.MOV",
                "fileSize": 120713028,
                "fileUrl": "https://material.geelark.cn/user-upload/497521349346987872/material-center/Ryzt3vkK14T5asJQPx2W.MOV",
                "fileType": 2,
                "width": 2160,
                "height": 3840,
                "source": 0,
                "tags": [
                    {
                        "id": "569577514586891738",
                        "name": "2",
                        "color": 2
                    }
                ],
                "userName": "Tom"
            }
        ]
    }
}
```


## Response Data Description


| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- 
| total | integer | total data |
| page | integer |current page  |
| pageSize | integer | current page size  |
| list | array[MaterialData] | material data |


## MaterialData Data Description


| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- 
| id | integer | material id |
| createdTime | integer | Creation time, second level timestamp |
| fileName | string | material name |
| fileSize | integer | material file size,  byte |
| fileUrl | string | material url |
| fileType | integer | material file type   1-image，2-video |
| width | integer | width |
| height | integer | height |
| source | integer | source: 0-upload，1-AI Edit 2Baidu  Cloud Drive 3GhostCut 4GoogleDrive 5Image to video |
| tags | array[TagData] | tag data |
| userName | string | upload user name |


## TagData Data Description


| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- |
| id | integer | tag id |
| name | integer |tag id  |
| color | integer | tag color: 0 White 1 Red 2 Blue 3 Green 4 Yellow 5 Purple |


## Error Codes


Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

#### Create tag

[TOC]

## Interface Description
create material tag


## Request URL

- `https://openapi.geelark.com/open/v1/material/tag/create`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description           | Example           |
| --- | --- | --- | --- | --- |
| name | Yes | string | tag name（Up to 30 characters） | Refer to Request Example  |
| color | No | int |  tag color: 0 White 1 Red 2 Blue 3 Green 4 Yellow 5 Purple | Refer to Request Example|

## Request Example
```json
{
    "name" : "test",
    "color" : 1
}
```


## Response Example

```json
{
    "traceId": "95D85F2085A6C847B2D68ABAAD591997",
    "code": 0,
    "msg": "success",
    "data": {
        "id": "570461738663674391"
    }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- 
| id | string | tag id |

## Error Codes

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 60002 | tag name repeat |

---

#### Delete tag

[TOC]

## Interface Description
delete material tag


## Request URL

- `https://openapi.geelark.com/open/v1/material/tag/del`

## Request Method
- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array[string] | tag id | Refer to Request Example  |


## Request Example
```json
{
    "ids" : ["570461738663674391"]
}
```


## Response Example

```json
{
  "traceId": "ACEB0CFEB887F99CB989BC9D9FF92BBC",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 2,
    "successAmount": 1,
    "failAmount": 1,
    "failDetails": [
      {
        "code": 43022,
        "id": "528953724308030464",
        "msg": "tag not found"
      }
    ]
  }
}
```


## Response Data Description
| Parameter Name | Type              | Description          |
| ------------- | ------------------ | ------------ |
| totalAmount    | integer           | Total delete requests |
| successAmount  | integer           | Total successes      |
| failAmount     | integer           | Total failures       |
| failDetails    | array[FailDetails] | Failure details      |


### Failure Details <FailDetails>


| Parameter Name | Type              | Description          |
| ------------ | ---------- | ------------ |
| code           | integer | Error code  |
| id             | string  | Tag ID     |
| msg            | string  | Error msg   |



## Error Codes
Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| ------ | ---------- |
| 43022  | tag not found |

---

#### Search material tag

[TOC]

## Interface Description
search material tag


## Request URL

- `https://openapi.geelark.com/open/v1/material/tag/search`


## Request Method
- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | No | int | page | Refer to Request Example  |
| pageSize | No | int | page size （max: 200） | Refer to Request Example  |
| name | No | string | search tag name | Refer to Request Example  |


## Request Example
```json
{
    "page" : 1,
    "pageSize" : 50 ,
    "name" : ""
}
```


## Response Example

```json
{
    "traceId": "8B6AC3809AAAE8099E94B124A7181BB9",
    "code": 0,
    "msg": "success",
    "data": {
        "total": 2,
        "page": 1,
        "pageSize": 50,
        "list": [
            {
                "id": "569577514586891738",
                "name": "2",
                "color": 4
            }
        ]
    }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- 
| total | int | total data |
| page | int |current page  |
| pageSize | int | current page size  |
| list | array[TagData] | tag data |

## TagData Data Description

| Parameter Name | Type              | Description          |
| ----------- | -----------|----------- |
| id | int | tag id |
| name | int |tag id  |
| color | int | tag color: 0 White 1 Red 2 Blue 3 Green 4 Yellow 5 Purple |


## Error Codes

Below are specific error codes for the API. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Cloud Phone API / Webhook

#### Instruction

[TOC]


- GeeLark will push some operation results to developers via Webhook. After setting the Webhook URL, developers can handle these events, For common callback types, please refer to:[Callback Type](https://open.geelark.com/api/callback-type "Callback Type")

### Interface Authentication
User-defined callback interface authentication is consistent with the authentication for requesting the Geelark API.

- The request method should be set to `POST`.
- Properly receive `request header information`.
- Only one of the token verification and key verification needs to be handled.
- Set `Content-Type` to `application/json`.

#### Required Request Headers for Key Verification

- `appId` Team AppId
- `traceId` Unique request ID
- `ts` Millisecond timestamp
- `nonce` Random number
- `sign` Signature result

#### Key Verification Parameter Generation Method

- `traceId` Use `Version 4 UUID`
- `nonce` Use the first 6 characters of `traceId`
- `sign` Concatenate the string `Team AppId` + `traceId` + `ts` + `nonce` + `Team AppKey`, and use the `SHA256` hexadecimal uppercase digest of the string

#### Token Verification

When making a request, the following request headers will be carried

- `traceId` Unique request ID
- `Authorization` Set to `Bearer: <The token value obtained from the GeeLark client>`

### Cloud Phone Start Callback Received Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| type | Yes | integer | Callback event type | 1: Boot event |
| id | Yes | string | Cloud Phone ID | See example |
| result | Yes | boolean | Execution result | true: Success, false: Failure |
| username | Yes | string | Username | admin@geelark.com |
| ip | Yes | string | user ip | 62.141.247.218 |
| eventTime | Yes | interger | Time stamp in seconds | 1766567054 |

#### Example of Cloud Phone Start Callback Received Parameters

```json
{
	"type": 1,
	"id": "528086321789535232",
	"result": true,
	"username" : "admin@geelark.com",
	"ip" : "62.141.247.218",
	"eventTime" : 1766567054
}
```

### Upload files to the cloud phone Callback Received Parameters

| Parameter Name | Description |
| --- | --- |
| type | 4: Plugin installation |
| id | Cloud Phone ID |
| taskId | Task ID |
| result | Execution result: true: Success, false: Failure |

#### Example of Upload files to the cloud phone Callback Received Parameters

```
{
    "type": 4,
    "id": "528715748189668352",
	"taskId": "128715748189668352",
    "result": true,
}
```

### Cloud phone screenshot callback Received Parameters

| Parameter Name | Description |
| --- | --- |
| type | 5 |
| id | Cloud Phone ID |
| taskId | Task ID |
| result | Execution result: true: Success, false: Failure |
| downloadLink | Download Link |

#### Example of Cloud phone screenshot callback Received Parameters

```
{
    "type": 5,
    "id": "528715748189668352",
	"taskId": "128715748189668352",
    "result": true,
	"downloadLink": "https://www.abc.com/a.jpg"
}
```


### Task completion Callback Received Parameters

| Parameter Name | Description |
| --- | --- |
| type | 6: Task completion |
| taskId | Task ID |
| result | Execution result: true: Success, false: Failure |

#### Example of Task completion Callback Received Parameters

```
{
    "type": 6,
	"taskId": "528715748189668352",
    "result": true
}
```

### Cloud Phone Stop  Callback Received Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| type | Yes | integer | Callback event type | 8: Stop event |
| id | Yes | string | Cloud phone ID | See example |
| username | Yes | string | Username | admin@geelark.com |
| ip | Yes | string | user ip | 62.141.247.218 |
| eventTime | Yes | interger | Time stamp in seconds | 1766567054 |
| useMin | Yes | interger |Usage duration (in minutes)| 12 |

#### Example of Cloud Phone Stop  Callback Received Parameters

```json
{     
	"type": 8,
	"id": "528086321789535232" ,
	"username" : "GeeLark",
	"ip" : "62.141.247.218",
	"eventTime" : 1766567054,
	"useMin": 1
}
```

### Cloud Phone Serial Name Change Callback Parameter

| Parameter Name | Description |
| --- | --- |
| type | 9: Cloud phone serial name change |
| id | Cloud Phone ID |
| name | New serial name |

#### Example of Cloud Phone Serial Name Change Callback Parameter

```
{
	"type": 9,
	"items": [
		{
			"id" : "583502967211075086",
			"name" : "newName"
		}
	]
}
```

### Cloud Phone Delete Callback Parameter

| Parameter Name | Description |
| --- | --- |
| type | 10: Cloud phone delete |
| id | Cloud Phone ID |
| recycle | Wether deleted to the trash |

#### Example of Cloud Phone Delete Callback Parameter

```
{
	"type": 10,
	"items": [
		{
			"id" : "583502967211075086",
			"recycle" : false
		}
	]
}
```

### Cloud Phone Tag Change Callback Parameters

| Parameter | Description |
| --- | --- |
| type | 11:Cloud Phone Tag Change|
| envIds | Array of cloud phone IDs |

#### Example of Cloud Phone Tag Change Callback Parameters

```
{
	"type": 11,
	"envIds" : ["583502967211075086"]
}
```

### Task Creation Callback Parameter Receiver

| Parameter | Description |
| --- | --- |
| type | The task creation callback type is 12 |
| taskIds | Task ID |
| channel | Triggering channel, api, client |

#### Example of Task Creation Callback Parameter Receiver

```
{
    "type": 12,
	"taskIds": ["528715748189668352"],
    "channel": "api"
}
```

### Task Cancellation Callback Parameter Receiver

| Parameter | Description |
| --- | --- |
| type | The task cancellation callback type is 13 |
| taskIds | Task ID |
| channel | Triggering channel, api, client |

#### Example of Task Cancellation Callback Parameter Receiver

```
{
    "type": 13,
	"taskIds": ["528715748189668352"],
    "channel": "api"
}
```

### Callback Parameters for Cloud Phone Batch Import Contacts

| Parameter | Description |
| --- | --- |
| type | Type value is 14 |
| taskId | Task ID |
| status | Status: 0 = Failed, 1 = Successful |

#### Example of Callback Parameters for Cloud Phone Batch Import Contacts
```
{
    "type": 14,
	"taskId": "528715748189168352",
    "status": 1
}
```

### Cloud phone app installation callback parameter reception

| Parameter | Description |
| --- | --- |
| type | type is 15 |
| packageName | Application package name |
| appVersionId | Application version ID |
| id | Cloud phone ID |
| result | Installation result, 0 failures, 1 success |

#### Example of receiving parameters during cloud phone app installation callback

```
{
	"type": 15,
	"packageName": "com.example.app",
	"appVersionId": "1793552962140770305",
	"id": "528715748189168352",
	"result": 1
}
```

---

#### Set Webhook URL

[TOC]

## Interface Description
Set the Webhook callback URL

## Request URL

- `https://openapi.geelark.com/open/v1/callback/set`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| url | Yes | string | Callback interface address | http://example.geelark.com/phone/callback/test |

## Request Example
```json
{
    "url": "http://example.geelark.com/phone/callback/test"
}
```

## Response Example

```json
{
    "traceId": "960B32039F84AA489514ADCC9ADA909F",
    "code": 0,
    "msg": "success"
}
```

---

#### Get Webhook URL

[TOC]

## Interface Description
Retrieve the callback interface URL set by the user.

## Request URL

- `https://openapi.geelark.com/open/v1/callback/get`

## Request Method

- POST

## Response Example

```json
{
    "traceId": "9CEA6CC9B5BB68BBAE4ABDF9BE5AC89D",
    "code": 0,
    "msg": "success",
    "data": {
        "url": "http://example.geelark.com/phone/callback/test"
    }
}
```

## Response Body Data Description

| Parameter Name | Type | Description |
| ----------- | ----------- | ----------- |
| url | string | The set callback URL |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 51001 | Callback URL not set |

---

#### Callback Type

| Callback Type | Event Value |
| --- | --- |
| Cloud phone startup callback | 1 |
| Cloud phone file upload callback | 4 |
| Cloud phone screenshot callback | 5 |
| Cloud phone RPA Task completion callback | 6 |
| Cloud phone shutdown callback | 8 |
| Cloud phone name change callback | 9 |
| Cloud phone deletion callback | 10 |
|Cloud phone tag change callback|11|
|Cloud phone RPA Task creation callback|12|
|Cloud phone RPA Task cancellation callback|13|
|Cloud Phone Batch Import Contacts Callback|14|
|Cloud Phone App Installation Callback|15|

---

### Cloud Phone API / OEM/White Label

#### OEM/White Label

[TOC]



## Interface Description
For anyone who want to integrate the 1st and world's best cloud phone, feel free to do it. Contact us if you need any help regarding integration.

Customize the brand name, brand logo, sidebar entrance, QR code domain name, etc.
- `You can access this feature when your plan includes 50 or more profiles.`


## Request URL


- `https://openapi.geelark.com/open/v1/phone/customization`


## Request Method


- POST


## Request Parameters


| Parameter Name | Required | Type          | Description           | Example           |
| -------------- | -------- | ------------- | --------------------- | ----------------- |
| title | No | string | Title, maximum length 64 bytes. If not provided or left empty, the original value remains unchanged. |  Refer to Request Example |
| logo | No | string |Logo URL, maximum length 255 bytes. If not provided or left empty, the original value remains unchanged.|  Refer to Request Example |
| hideHeader | No | bool | Whether to hide the header at the top of the cloud phone. Defaults to false if not provided|  false|
|mirrorUrl|No|string|The QR code and the url opened on the phone's browser in the "Mirror" entrance, limited to 255 characters. if set this value, GeeLark will display the url in the "Mirror" entrance (as shown picture blow).![demo](https://singapore-upgrade.geelark.cn/en_mirror_url_demo.jpg "demo") When open this url, please redirect to https://mobile.geelark.com/mobile.html with all parameters (it is recommended to use a iframe) )|Refer to Request Example|
| toolBarSettings | No | array[ToolBarSettings] | Control whether the toolbar entrance on the side of the cloud phone should displayed. If not set, all will be displayed by default. | See request example |

### mirrorUrl
If set the 'mirrorUrl' as `https://www.xxx.com/mobile.html`  the link in 'Mirror' entrance will be 
`https://www.xxx.com/mobile.html?envirId=xxx&localeCode=en_US&userId=xxx5&traceId=xxx&token=xxx&env=prod&qcode=true&check=success` 
When users access this link, you need to embed an iframe on the current page and set the src attribute to 
`https://mobile.geelark.com/mobile.html?envirId=xxx&localeCode=en_US&userId=xxx5&traceId=xxx&token=xxx&env=prod&qcode=true&check=success` 
Then user can open this profile

### ToolBarSettings
| Parameter | Type | Description |
| --- | --- | --- |
| toolBar | string | Toolbar item name. Refer to the item descriptions below. |
| visible | bool | Whether to display the item. If omitted or set to false, the item will not be displayed. |
| iconUrl | string | Icon URL, maximum length 255 bytes; if not provided or left empty, the original value will remain unchanged; supported formats: SVG, PNG, JPG (SVG is recommended). Recommended size: 16×16 |

#### Toolbar Item Descriptions
*   `networkQuality`: Network quality indicator
*   `rotate`: Rotate
*   `screenshot`: Screenshot
*   `upload`: File upload
*   `library`: library. This setting takes effect only when upload is visible; hiding it is effective only in that case.
*   `volumeUp`: Volume up
*   `volumeDown`: Volume down
*   `speedUp`: Speed up
*   `detection`: Network detection
*   `quality`: Video quality
*   `restart`: Restart
*   `appStore`: Application (management)
*   `qcode`: QR code
*   `export`: Export
*   `timing`: Timer
*   `liveStreaming`: Live streaming (recording)
*   `clear`: Clear
*   `teamApp`: Team's applications


## Request Example
```json
{
    "logo": "https://material.geelark.cn/user-upload/banner0903_cn.jpg",
    "title": "GeeLark",
    "hideHeader": false,
    "mirrorUrl": "https://www.abcd.com/mirror/url",
	"toolBarSettings": [
        {
            "toolBar": "networkQuality",
            "visible": false
        },
		 {
            "toolBar": "rotate",
            "visible": false
        },
		 {
            "toolBar": "screenshot",
            "visible": false
        },
		 {
            "toolBar": "upload",
            "visible": true
        },
		 {
            "toolBar": "library",
            "visible": false
        },
		 {
            "toolBar": "volumeUp",
            "visible": false
        }
    ]
}
```


## Response Example


```json
{
    "traceId": "ADD9A7489BB2198DBC0FB37082684CB0",
    "code": 0,
    "msg": "success"
}
```



## Error Codes


Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).


| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 40015 | Permission limit |
| 60003 | Illegal url |
| 60004 | Invalid file format |

---

### Cloud Phone API / Analytics

#### Get account data

[TOC]

## API Description

Get account data

## Request URL

*    `https://openapi.geelark.com/open/v1/analytics/data`

## Request Method

*   POST

## Request Parameters

### Query Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page   | Yes   | integer | page | 1 |
| pageSize   | Yes   | integer | page size（1-100） | 10 |
| account   | No   | string | account| tk_acc |
| dataDate   | No   | integer | search date timestamp | 1764136841 |
| createdId   | No   | string | user add account user id  | 547236295441737181 |
| channel   | No   | integer | account channel, 0: TikTok 1:YouTube 2:Instagram | 1 |

## Request Example
```json
{
	"account" : "tk_acc",
	"dataDate" : 1764137986,
	"createdId" : "497521349330210656",
	"channel" : 1,
	"page" : 1,
	"pageSize" : 10
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total    | integer               | total |
| page  | integer               | current page      |
| pageSize     | integer               | current page size     |


### successDetails Success Information <items>

| Parameter Name | Type | Description |
| --- | --- | --- |
| id    | string               | account id |
| channel  | integer               | account channel     |
| account     | string               | account     |
| playCount     | integer               | play count ,  -1 indicates that the data has not been updated yet|
| followerCount     | integer               | follower count  ,  -1 indicates that the data has not been updated yet    |
| diggCount     | integer               | digg count  ,  -1 indicates that the data has not been updated yet    |
| commentCount     | integer               | comment count   ,  -1 indicates that the data has not been updated yet   |
| collectCount     | integer               | collect count   ,  -1 indicates that the data has not been updated yet   |
| shareCount     | integer               | share count  ,  -1 indicates that the data has not been updated yet    |
| dataDate     | integer               | data date     |
| addAccDate     | integer               | add account date     |
| remark     | string               | remark     |
| createdId     | string               | add account user id     |
| username     | string               | add account username     |


## Response Example

```json
{
	"traceId": "B8899554AA90BB168406A5CB8A089AB2",
	"code": 0,
	"msg": "success",
	"data": {
		"total": 2,
		"page": 1,
		"pageSize": 10,
		"items": [
			 {
				 "id": "581465531480044822",
				 "channel": 0,
				 "account": "khian.kb",
				 "playCount": -1,
				 "followerCount": -1,
				 "diggCount": -1,
				 "commentCount": -1,
				 "collectCount": -1,
				 "shareCount": -1,
				 "dataDate": -1,
				 "addAccDate": 1756110064,
				 "remark": "",
				 "createdId": "497521349330210656",
				 "username": "exlrhoo@foxmail.com"
			 }
		 ]
	}
}
```

## Error Codes

Below are specific error codes for this interface. For other error codes, please refer to [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description |
| --- | --- |
| 43002  | please upgrade to pro package, then try again   |

---

#### Add Accounts

[TOC]

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/analytics/accounts/add`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| channel | Yes | integer | Platform | 0: TikTok, 1: YouTube, 2: Instagram |
| accountsData | Yes | array\[accountsData\] | Account information. The array supports up to 200 elements | See request example |

### accountsData

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| account | Yes | string | Account name, maximum length 64 characters | See request example |
| remark | No | string | Remark information | See request example |

Request Example
---------------

```json
{
    "channel":0,
    "accountsData": [
        {
            "account":"XXX",
            "remark":"remark xxx"
        }
    ]
}
```
Response Parameters
-------------------

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| bizCode | Yes | integer | Business status code: 0 = all successful; 1 = the current number of accounts exceeds the limit; 2 = partially successful, with failed items exceeding the limit |
| successCount | Yes | integer | Number of successfully added accounts |
| failCount | Yes | integer | Number of failed additions |
| repeatCount | Yes | integer | Number of duplicate additions |

Response Example
----------------

```json
{
	"traceId": "9D1A84D6A2A8F9A8A5CD9BA7B7E84281",
	"code": 0,
	"msg": "success",
	"data": {
    	"bizCode": 0,
    	"successCount": 1,
    	"failCount": 0,
    	"repeatCount": 0
	}
}
```

---

#### Delete Account

[TOC]

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/analytics/accounts/delete`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| channel | Yes | integer | Platform | 0: TikTok, 1: YouTube, 2: Instagram |
| account | Yes | string | Account name, maximum length 64 characters | See request example |

Request Example
---------------

```json
{
    "channel":0,
    "account":"xxxx"
}
```

Response Example
----------------

```json
{
	"traceId": "9D1A84D6A2A8F9A8A5CD9BA7B7E84281",
	"code": 0,
	"msg": "success"
}
```

---

#### Accounts List

[TOC]

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/analytics/accounts/list`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | Yes | integer | Page number | 1 |
| pageSize | Yes | integer | Number of items per page (1–100) | 10 |
| account | No | string | Account name | tk\_acc |
| channel | No | integer | Platform, if not provided all platforms are included | 0: TikTok 1: YouTube 2: Instagram |
| userAccount | No | string | Operator account | abc@gmail.com |

Request Example
---------------
```json
{
    "page":1,
    "pageSize":10,
    "channel":1
}
```

Response Data Description
-------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total count |
| page | integer | Current page |
| items | array\[item\] | Account data |

Response Data Description <item>
--------------------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Account ID |
| account | string | Account |
| channel | integer | Platform: 0: TikTok 1: YouTube 2: Instagram |
| remark | string | Remark |
| operator | string | Username of the last operator |
| created\_time | integer | Creation time |
| updated\_time | integer | Last update time |

Response Example
----------------

```json
{
    "traceId": "99793C8DABAC5970A91693E38BBA0596",
    "code": 0,
    "msg": "success",
    "data": {
        "items": [
            {
                "id": "565523829426802069",
                "account": "xxx",
                "channel": 1,
                "remark": "remark",
                "operator": "xxx",
                "created_time": 1746608069,
                "updated_time": 1746608069
            }
        ],
        "total": 1,
        "page": 1
    }
}
```

---

#### Update Account

[TOC]

## Request URL

- `https://openapi.geelark.com/open/v1/analytics/accounts/update`

## Request Method

- POST

## Request Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Account ID | 565523829426802069 |
| account | No | string | Platform account, maximum 64 characters | myAccount |
| channel | No | integer | Platform | 0: TikTok 1: YouTube 2: Instagram |
| remark | No | string | Remark | myRemark |

## Request Example

```json
{
    "id": "565523829426802069",
    "account": "abc"
}
```

## Response Example

```json
{
    "traceId": "9D1A84D6A2A8F9A8A5CD9BA7B7E84281",
    "code": 0,
    "msg": "success"
}
```

---

### Browser API / Browser Management

#### Create new browser

[TOC]


## Interface Description


Create a new browser, support configuration of platform account password and cookies, proxy ID and proxy information, fingerprint information, etc. After successful creation, the browser environment ID is returned.



## Request URL


- `http://localhost:40185/api/v1/browser/create`


## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| serialName | Yes | string | Environment name, up to 100 characters | myBrowser |
| groupId | No | string | Environment group ID | 497548067550006541 |
| tagIds | No | array[string] | Environment tag IDs | ["497548067550006541"] |
| remark | No | string | Environment remark, up to 1500 characters | myRemark |
| cookie | No | string | Cookie, supports JSON and Netscape formats | [{"domain":".example.com","expires":"2025-12-31T23:59:59Z","httpOnly":true,"name":"SESSION_ID","path":"/","sameSite":"Lax","secure":true,"value":"a1b2c3d4e5f67890abcdef1234567890"}] |
| accountPlatform | No | string | Account platform. Only supports https://www.tiktok.com/ and https://www.facebook.com/ | https://www.tiktok.com/ |
| accountUsername | No | string | Account username | myUser |
| accountPassword | No | string | Account password | myPass |
| accountTOTPSecret | No | string | Account 2FA key | 7J64V3P3E77J3LKNUGSZ5QANTLRLTKVL |
| openLastPage | No | integer | Whether to restore the last visit, 1-Yes, 2-No, default is No | 1 |
| openSpecPage | No | integer | Whether to open the specified URL, 1-Yes, 2-No, default is No | 1 |
| openTabs | No | string | Opens specified web pages. Separate multiple tabs with ;. | http://www.b.com |
| browserOs | Yes | integer | Operating system, 1-win, 2-mac | 1 |
| browserUa | No | string | userAgent, if not passed, a random value will be used | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.93 Safari/537.36 |
| simulateConfig | No | SimulateConfig | Simulation configuration, if not passed, a random value will be used | See SimulateConfig |
| proxyId | No | string | Proxy ID, preferred | 497548067550006541 |
| proxyConfig | No | BrowserApiAddProxy | Proxy information | See BrowserApiAddProxy |
| browserStartArg | No | string | Startup parameters | -disable-popups |


###  Simulation Configuration SimulateConfig


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| timeZone | Yes | object | Time zone | - |
| timeZone.switcher | Yes | integer | 1: Matched by IP address, 2: Custom, 3: Local time zone | 2 |
| timeZone.value | Yes | string | Custom value, refer to [Browser Timezone](https://singapore-upgrade.geelark.cn/apiResource/browser_timezone.txt) | GMT-12:00 Etc/GMT+12 |
| language | Yes | object | Language | - |
| language.switcher | Yes | integer | 1: Matched by IP address, 2: Custom | 2 |
| language.value | Yes | string | Custom value, multiple values separated by commas, refer to [Browser Language](https://singapore-upgrade.geelark.cn/apiResource/browser_language.txt) | Albanian |
| resolution | Yes | object | Resolution | - |
| resolution.switcher | Yes | integer | 1: Random, 2: Custom, 3: Default | 2 |
| resolution.value | Yes | string | Custom value, refer to [browser resolution](https://singapore-upgrade.geelark.cn/apiResource/browser_resolution.txt) | 750*1334 |
| webRtc | yes | object | WebRTC | - |
| webRtc.switcher | yes | integer | 1: Privacy, 2: Replace, 3: True, 4: Disable | 1 |
| geoLocation | yes | object | Geolocation | - |
| geoLocation.switcher | yes | integer | 1: Ask, 2: Disable, 3: Allow | 1 |
| geoLocation.baseOnIp | yes | bool | Match based on IP | true |
| geoLocation.longitude | yes | integer | Latitude | 10 |
| geoLocation.latitude | yes | integer | Longitude | 20 |
| geoLocation.accuracy | yes | integer | Accuracy (meters) | 10 |
| canvas | yes | object | Canvas | - |
| canvas.switcher | yes | integer | 1: Noise, 2: True | 1 |
| webglImage | yes | object | WebGL Image | - |
| webglImage.switcher | Yes | integer | 1: Noise, 2: Real | 1 |
| hardware | Yes | object | Hardware Acceleration | - |
| hardware.switcher | Yes | integer | 1: Default, 2: Enabled, 3: Disabled | 1 |
| audioContext | Yes | object | AudioContext | - |
| audioContext.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| mediaDevice | Yes | object | Media Device | - |
| mediaDevice.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| clientRects | Yes | object | ClientRects | - |
| clientRects.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| speechVoise | Yes | object | SpeechVoices | - |
| speechVoise.switcher | Yes | integer | 1: Noise, 2: Off | 1 |
| hardwareConcurrency | Yes | integer | Hardware concurrency | 26 |
| memoryDevice | Yes | integer | Device memory | 8 |
| doNotTrack | Yes | integer | Do Not Track 0: Default, 1: On, 2: Off | 2 |
| bluetooth | Yes | object | Bluetooth | - |
| bluetooth.switcher | Yes | integer | 1: Privacy, 2: True | 1 |
| battery | Yes | object | Battery | - |
| battery.switcher | Yes | integer | 1: Privacy, 2: True | 1 |
| portScanProtection | Yes | object | Port scan protection | - |
| portScanProtection.switcher | Yes | integer | 1: Enable, 2: Disable | 1 |
| portScanProtection.value | Yes | string | Ports allowed to be scanned, comma separated | 80 |


### Proxy Information BrowserApiAddProxy


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| typeId | yes | integer | Proxy type ID. -1 represents a direct connection. | 1 |
| server | no | string | Proxy host | server.com |
| port | no | integer | Proxy port | 1234 |
| username | no | string | Proxy username | user |
| password | no | string | Proxy password | password |
| country | no | string | Dynamic proxy country | us |
| region | no | string | Dynamic proxy region | alabama |
| city | no | string | Dynamic proxy city | mobile |
| useProxyCfg | no | bool | Whether to use the configured dynamic proxy. | true |
| protocol | no | integer | Dynamic proxy protocol. 1 represents socks5, 2 represents http. | 1 |


### Proxy type id


- `-1` Direct connection
- `1` socks5
- `2` http
- `3` https
- `20` IPIDEA Proxy
- `21` IPHTML Proxy
- `22` kookeey Proxy
- `23` Lumatuo Proxy



## Request Example



```json
{
    "serialName":"myBrowserName",
    "browserOs":1,
    "proxyConfig":{
        "typeId":-1
    },
    "simulateConfig":{
        "timeZone": {
            "switcher": 2,
            "value": "GMT-12:00 Etc/GMT+12"
        },
        "language": {
            "switcher": 2,
            "value": "Albanian"
        },
        "resolution": {
            "switcher": 2,
            "value": "750*1334"
        },
        "webRtc":{
            "switcher":1
        },
        "geoLocation":{
            "switcher":1,
            "baseOnIp":true,
            "longitude":20,
            "latitude":10,
            "accuracy":1
        },
        "canvas":{
            "switcher":1
        },
        "webglImage":{
            "switcher":1
        },
        "hardware":{
            "switcher":1
        },
        "audioContext":{
            "switcher":1
        },
        "mediaDevice":{
            "switcher":1
        },
        "clientRects":{
            "switcher":1
        },
        "speechVoise":{
            "switcher":1
        },
        "hardwareConcurrency":26,
        "memeryDevice":8,
        "doNotTrack":2,
        "bluetooth":{
            "switcher":1
        },
        "battery":{
            "switcher":1
        },
        "portScanProtection":{
            "switcher":1,
            "value":"80"
        }
    }
}
```



## Example response



```json
{
    "traceId":"123456ABCDEF",
    "code":0,
    "msg":"success",
    "data":{
        "id":"497548067550006541"
    }
}
```



## Response body data description



| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Environment ID |



## Error Code



Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).



| Error Code | Description |
| --- | --- |
| 44002 | The maximum number of package environments has been reached |
| 44003 | The maximum number of user environments has been reached |
| 44004 | The maximum number of environments created today has been reached |
| 45006 | Incorrect proxy information |
| 45003 | Proxy not allowed |
| 45004 | Proxy verification failed |
| 43028 | The sub-user does not have permissions for this environment group |

---

#### Edit browser

[TOC]


## Interface Description


Modify environment information, support updating account passwords and cookies, proxy information, fingerprint information, etc.



## Request URL


- `http://localhost:40185/api/v1/browser/update`


## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Environment id | 497548067550006541 |
| serialName | No | string | Environment name. If left blank, no change. Maximum 100 characters. | myBrowser |
| groupId | No | string | Environment group id. If omitted, no change. If left blank, the environment is marked as ungrouped. | 497548067550006541 |
| tagIds | No | array[string] | Environment tag ids. If omitted, no change. If left blank, the environment is marked as untagless. | ["497548067550006541"] |
| remark | No | string | Environment remark. Maximum 1500 characters. If left blank, no change. | myRemark |
| cookie | No | string | Cookie. Supports JSON and Netscape formats. | [{"domain":".example.com","expires":"2025-12-31T23:59:59Z","httpOnly":true,"name":"SESSION_ID","path":"/","sameSite":"Lax","secure":true,"value":"a1b2c3d4e5f67890abcdef1234567890"}] |
| accountPlatform | No | string | Account platform. Will not be changed if not passed. Only supports https://www.tiktok.com/, https://www.facebook.com/ | https://www.tiktok.com/ |
| accountUsername | No | string | Account username. Valid only when accountPlatform is valid. | myUser |
| accountPassword | No | string | Account password. Valid only when accountPlatform is valid. | myPass |
| accountTOTPSecret | No | string | Account 2FA key, only effective if accountPlatform is valid. If not provided, it will not be changed; if empty, it will be left blank. | 7J64V3P3E77J3LKNUGSZ5QANTLRLTKVL |
| openLastPage | No | integer | Restore last access, 1-Yes, 2-No | 1 |
| openSpecPage | No | integer | Open specified URL, 1-Yes, 2-No | 1 |
| openTabs | No | string | Opens the specified webpages. Separate multiple pages with ";". If not passed, no changes will be made. | http://www.b.com |
| browserOs | No | integer | Operating system. If not passed, no changes will be made. 1-win, 2-mac | 1 |
| browserUa | No | string | UserAgent. If not passed, no changes will be made. | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.93 Safari/537.36 |
| simulateConfig | No | SimulateConfig | Simulate configuration. If not passed, no changes will be made. | See SimulateConfig |
| proxyId | No | string | Proxy ID. Used first. If neither proxyId nor proxyConfig is passed, no changes will be made to the proxy. | 497548067550006541 |
| proxyConfig | No | BrowserApiAddProxy | Proxy information. If neither proxyId nor proxyConfig is passed, the proxy will not be modified. | See BrowserApiAddProxy |
| browserStartArg | No | string | Startup parameters; if not passed, they will not be modified. | -disable-popups |


###  Simulation Configuration SimulateConfig


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| timeZone | Yes | object | Time zone | - |
| timeZone.switcher | Yes | integer | 1: Matched by IP address, 2: Custom, 3: Local time zone | 2 |
| timeZone.value | Yes | string | Custom value, refer to [Browser Timezone](https://singapore-upgrade.geelark.cn/apiResource/browser_timezone.txt) | GMT-12:00 Etc/GMT+12 |
| language | Yes | object | Language | - |
| language.switcher | Yes | integer | 1: Matched by IP address, 2: Custom | 2 |
| language.value | Yes | string | Custom value, multiple values separated by commas, refer to [Browser Language](https://singapore-upgrade.geelark.cn/apiResource/browser_language.txt) | Albanian |
| resolution | Yes | object | Resolution | - |
| resolution.switcher | Yes | integer | 1: Random, 2: Custom, 3: Default | 2 |
| resolution.value | Yes | string | Custom value, refer to [browser resolution](https://singapore-upgrade.geelark.cn/apiResource/browser_resolution.txt) | 750*1334 |
| webRtc | yes | object | WebRTC | - |
| webRtc.switcher | yes | integer | 1: Privacy, 2: Replace, 3: True, 4: Disable | 1 |
| geoLocation | yes | object | Geolocation | - |
| geoLocation.switcher | yes | integer | 1: Ask, 2: Disable, 3: Allow | 1 |
| geoLocation.baseOnIp | yes | bool | Match based on IP | true |
| geoLocation.longitude | yes | integer | Latitude | 10 |
| geoLocation.latitude | yes | integer | Longitude | 20 |
| geoLocation.accuracy | yes | integer | Accuracy (meters) | 10 |
| canvas | yes | object | Canvas | - |
| canvas.switcher | yes | integer | 1: Noise, 2: True | 1 |
| webglImage | yes | object | WebGL Image | - |
| webglImage.switcher | Yes | integer | 1: Noise, 2: Real | 1 |
| hardware | Yes | object | Hardware Acceleration | - |
| hardware.switcher | Yes | integer | 1: Default, 2: Enabled, 3: Disabled | 1 |
| audioContext | Yes | object | AudioContext | - |
| audioContext.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| mediaDevice | Yes | object | Media Device | - |
| mediaDevice.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| clientRects | Yes | object | ClientRects | - |
| clientRects.switcher | Yes | integer | 1: Noise, 2: Disabled | 1 |
| speechVoise | Yes | object | SpeechVoices | - |
| speechVoise.switcher | Yes | integer | 1: Noise, 2: Off | 1 |
| hardwareConcurrency | Yes | integer | Hardware concurrency | 26 |
| memoryDevice | Yes | integer | Device memory | 8 |
| doNotTrack | Yes | integer | Do Not Track 0: Default, 1: On, 2: Off | 2 |
| bluetooth | Yes | object | Bluetooth | - |
| bluetooth.switcher | Yes | integer | 1: Privacy, 2: True | 1 |
| battery | Yes | object | Battery | - |
| battery.switcher | Yes | integer | 1: Privacy, 2: True | 1 |
| portScanProtection | Yes | object | Port scan protection | - |
| portScanProtection.switcher | Yes | integer | 1: Enable, 2: Disable | 1 |
| portScanProtection.value | Yes | string | Ports allowed to be scanned, comma separated | 80 |


### Proxy Information BrowserApiAddProxy


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| typeId | yes | integer | Proxy type ID. -1 represents a direct connection. | 1 |
| server | no | string | Proxy host | server.com |
| port | no | integer | Proxy port | 1234 |
| username | no | string | Proxy username | user |
| password | no | string | Proxy password | password |
| country | no | string | Dynamic proxy country | us |
| region | no | string | Dynamic proxy region | alabama |
| city | no | string | Dynamic proxy city | mobile |
| useProxyCfg | no | bool | Whether to use the configured dynamic proxy. | true |
| protocol | no | integer | Dynamic proxy protocol. 1 represents socks5, 2 represents http. | 1 |


### Proxy type id


- `-1` Direct connection
- `1` socks5
- `2` http
- `3` https
- `20` IPIDEA Proxy
- `21` IPHTML Proxy
- `22` kookeey Proxy
- `23` Lumatuo Proxy



## Request Example



```json
{
    "id":"497548067550006541",
    "simulateConfig":{
        "timeZone": {
            "switcher": 2,
            "value": "GMT-12:00 Etc/GMT+12"
        },
        "language": {
            "switcher": 2,
            "value": "Albanian"
        },
        "resolution": {
            "switcher": 2,
            "value": "750*1334"
        },
        "webRtc":{
            "switcher":1
        },
        "geoLocation":{
            "switcher":1,
            "baseOnIp":true,
            "longitude":20,
            "latitude":10,
            "accuracy":1
        },
        "canvas":{
            "switcher":1
        },
        "webglImage":{
            "switcher":1
        },
        "hardware":{
            "switcher":1
        },
        "audioContext":{
            "switcher":1
        },
        "mediaDevice":{
            "switcher":1
        },
        "clientRects":{
            "switcher":1
        },
        "speechVoise":{
            "switcher":1
        },
        "hardwareConcurrency":26,
        "memeryDevice":8,
        "doNotTrack":2,
        "bluetooth":{
            "switcher":1
        },
        "battery":{
            "switcher":1
        },
        "portScanProtection":{
            "switcher":1,
            "value":"80"
        }
    }
}
```



## Example response



```json
{
  "traceId": "123456ABCDEF",
  "code": 0,
  "msg": "success"
}
```



## Error Code



Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).



| Error Code | Description |
| --- | --- |
| 45006 | Proxy information error |
| 45003 | Proxy not allowed |
| 45004 | Proxy verification failed |
| 43028 | The sub-user does not have permissions for this environment group |

---

#### Delete browser

[TOC]

## Interface Description

Delete unnecessary environments. Batch deletion is supported, but the number of environments that can be deleted at one time cannot exceed 100.


## Request URL

- `http://localhost:40185/api/v1/browser/delete`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| envIds | Yes | array[string] | Browser ID array, up to 100 | [“539893235657500146”] |


## Request Example


```json
{
  "envIds": ["539893235657500146"]
}
```


## Example response


```json
{
	"traceId":"123456ABCDEF",
	"code":0,
	"msg":"success",
	"data":{
		"busyIds":["539893235657500146"],
		"serverErrIds":["539893235657500147"],
		"successIds":["539893235657500148"]
	}
}
```


## Response body data description


| Parameter Name | Type | Description |
| --- | --- | --- |
| successIds | array[string] | IDs of environments that were successfully deleted |
| busyIds | array[string] | IDs of environments currently in use |
| serverErrIds | array[string] | IDs of environments handling exceptions |


## Error Code


Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

| Error Code | Description |
| --- | --- |
| 43028 | The sub-user does not have the permission of the environment group |

---

#### Get browser list

[TOC]


## Interface Description


Query the created environment information, including agent information, agent ID, etc.



## Request URL


- `http://localhost:40185/api/v1/browser/list`


## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | No | integer | Page number, minimum is 1, defaults to 1 if left blank | 1 |
| pageSize | No | integer | Number of records per page, minimum is 1, maximum is 100, defaults to 10 if left blank | 10 |
| ids | No | array[string] | Environment IDs, maximum is 100. Pagination parameters are used only if left blank | ["5213214343124321"] |
| serialName | No | string | Environment name | myEnv |
| remark | No | string | Remark | myRemark |
| groupName | No | string | Group name | myGroup |
| tags | No | array[string] | Array of tag names | ["myTag"] |



## Request Example



```json
{
 "page": 1,
 "pageSize": 10
}
```



## Example response



```json
{
    "traceId":"Zt0YNAeHR",
    "code":0,
    "msg":"success",
    "data":{
        "total":1,
        "page":1,
        "pageSize":10,
        "items":[
            {
                "id":"5213214343124321",
                "serialName":"myEnv",
                "serialNo":"3",
                "group":{
                    "id":"5213214343124321",
                    "name":"myGroup",
                    "remark":"myRemark"
                },
                "remark":"myRemark",
                "tags":[
                    {
                        "name":"myTag"
                    }
                ],
                "proxy":{
                    "type":"",
                    "server":"",
                    "port":0,
                    "username":"",
                    "password":""
                },
                "accountInfo":{
                    "url":"https://www.tiktok.com/",
                    "userName":"jay",
                    "passWord":"password",
                    "totpSecret": "",
                    "afterStartup":3,
                    "openLastPage": 2,
                    "openSpecPage": 1,
                    "openSiteUrl": true,
                    "autoOpenUrls":["http://www.b.com"]
                },
                "simulateInfo":{
                    "os":2,
                    "vendor":1,
                    "mixtureKey":"87da5186e1feabc1",
                    "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.141 Safari/537.36",
                    "uaVersion":"133",
                    "timeZone":{
                        "switcher":2,
                        "value": "GMT-12:00 Etc/GMT+12"
                    },
                    "webRtc":{
                        "switcher":1
                    },
                    "geoLocation":{
                        "switcher":1,
                        "baseOnIp":true,
                        "longitude":20,
                        "latitude":10,
                        "accuracy":1
                    },
                    "language":{
                        "switcher":2,
                        "value": "Albanian"
                    },
                    "resolution":{
                        "switcher":2,
                        "value": "750*1334"
                    },
                    "font":{
                        "switcher":2
                    },
                    "canvas":{
                        "switcher":1
                    },
                    "webglImage":{
                        "switcher":1
                    },
                    "webglMetadata":{
                        "switcher":3,
                        "provider":"Google Inc. (Intel Inc.)",
                        "render":"ANGLE (Intel Inc., Intel(R) HD Graphics 6000, OpenGL 4.1)"
                    },
                    "hardware":{
                        "switcher":1
                    },
                    "audioContext":{
                        "switcher":1
                    },
                    "mediaDevice":{
                        "switcher":1
                    },
                    "clientRects":{
                        "switcher":1
                    },
                    "speechVoise":{
                        "switcher":1
                    },
                    "hardwareConcurrency":26,
                    "memeryDevice":8,
                    "doNotTrack":2,
                    "bluetooth":{
                        "switcher":1
                    },
                    "battery":{
                        "switcher":1
                    },
                    "portScanProtection":{
                        "switcher":1,
                        "value":"80"
                    }
                }
            }
        ]
    }
}
```



## Response body data description



| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of data |
| page | integer | Current page number |
| pageSize | integer | Number of data items per page |
| items | array[BrowserApiSearchSimpleItem] | Data list |


### Browser data BrowserApiSearchSimpleItem


| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Environment id |
| serialName | string | Environment name |
| serialNo | string | Environment number |
| group | EnvGroup | Environment group |
| remark | string | Remark |
| tags | array[EnvTag] | Environment tags |
| proxy | EnvPhoneListProxy | Proxy information |
| accountInfo | BrowserApiSearchSimpleAccount | Account information |
| simulateInfo | BrowserApiSearchSimpleSimulate | Simulation information |


### Environmental Grouping EnvGroup


| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Environment group id |
| name | string | Environment group name |
| remark | string | Environment group remark |


### Environmental Label EnvTag


| Parameter Name | Type | Description |
| --- | --- | --- |
| name | string | Tag Name |


### Proxy Information EnvPhoneListProxy


| Parameter Name | Type | Description |
| --- | --- | --- |
| type | string | Proxy type |
| server | string | Proxy host |
| port | integer | Proxy port |
| username | string | Proxy username |
| password | string | Proxy password |


### Account Information BrowserApiSearchSimpleAccount


| Parameter Name | Type | Description |
| --- | --- | --- |
| url | string | Platform address |
| userName | string | Platform account |
| passWord | string | Platform password |
| totpSecret | string | 2FA key |
| afterStartup | integer | Page to open after startup. 1 - Restore last access, 2 - Open the specified URL, 3 - Open the specified URL and the platform page simultaneously, 4 - Restore last access and the platform page simultaneously. This field is obsolete. |
| openLastPage | integer | Restore last visit 1 Yes 2 No |
| openSpecPage | integer | Open specified URL 1 Yes 2 No |
| openSiteUrl | bool | Open platform page |
| autoOpenUrls | array[string] | Specified URL |


### Simulation Information BrowserApiSearchSimpleSimulate


| Parameter Name | Type | Description |
| --- | --- | --- |
| os | integer | Operating system, 1: Win, 2: Mac |
| vendor | integer | Browser type, 1: Chrome |
| mixtureKey | string | Fingerprint algorithm ID |
| ua | string | User agent |
| uaVersion | string | Browser version, 0 represents all |
| timeZone | object | Time zone |
| timeZone.switcher | integer | 1: IP-based matching, 2: Custom, 3: Local timezone |
| timeZone.value | string | Custom value |
| webRtc | object | WebRTC |
| webRtc.switcher | integer | 1: Privacy, 2: Replace, 3: Real, 4: Disable |
| geoLocation | object | Geolocation |
| geoLocation.switcher | integer | 1: Ask, 2: Disable, 3: Allow |
| geoLocation.baseOnIp | bool | Match based on IP address |
| geoLocation.longitude | integer | Latitude |
| geoLocation.latitude | integer | Longitude |
| geoLocation.accuracy | integer | Accuracy (meters) |
| language | object | Language |
| language.switcher | integer | 1: IP-based matching, 2: Custom |
| language.value | string | A custom value, multiple values separated by commas |
| resolution | object | Resolution |
| resolution.switcher | integer | 1: random, 2: custom, 3: default |
| resolution.value | string | custom value |
| font | object | Font |
| font.switcher | integer | 1: Default, 2: Custom |
| canvas | object | Canvas |
| canvas.switcher | integer | 1: Noise, 2: Real |
| webglImage | object | WebGL Image |
| webglImage.switcher | integer | 1: Noise, 2: Real |
| webglMetadata | object | WebGL Metadata |
| webglMetadata.switcher | integer | 2: Disabled, 3: Custom |
| webglMetadata.provider | string | WebGL Provider |
| webglMetadata.render | string | WebGL Rendering |
| hardware | object | Hardware acceleration |
| hardware.switcher | integer | 1: Default, 2: Enabled, 3: Disabled |
| audioContext | object | AudioContext |
| audioContext.switcher | integer | 1: Noise, 2: Disabled |
| mediaDevice | object | Media device |
| mediaDevice.switcher | integer | 1: Noise, 2: Disabled |
| clientRects | object | ClientRects |
| clientRects.switcher | integer | 1: Noise, 2: Disabled |
| speechVoise | object | SpeechVoices |
| speechVoise.switcher | integer | 1: Noise, 2: Disabled |
| hardwareConcurrency | integer | Hardware concurrency |
| memoryDevice | integer | Device memory |
| doNotTrack | integer | Do Not Track 0: Default, 1: Enabled, 2: Disabled |
| bluetooth | object | Bluetooth |
| bluetooth.switcher | integer | 1: Private, 2: True |
| battery | object | Battery |
| battery.switcher | integer | 1: Private, 2: True |
| portScanProtection | object | Port scan protection |
| portScanProtection.switcher | integer | 1: Enable, 2: Disable |
| portScanProtection.value | string | Comma-separated list of ports allowed to be scanned |



## Error Code



Please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

---

#### Launch browser

[TOC]

## Interface Description

Used to start the browser environment with the specified ID. Supports synchronous response and asynchronous WebHook callback notification.

## Request URL

- `http://localhost:40185/api/v1/browser/start`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | browser id| 539893235657500146 |
|webhook|No|string|Callback URL. Notification will be sent after the browser finishes starting|http://localhost:3001

##WebHook Callback
###Trigger Timing
Triggered after the browser startup task is completed.
###Callback URL
Specified by the webhook request parameter.
###Callback Method
POST
###Callback Request Headers
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer AZ4LY7J33IY5NQ7IYVQ5D5BR7B6GNWSG" // Same as the Authorization header in the API request
}
```
###Callback Data
```json
{
  "event": "browser_start",
  "timestamp": 1776147008407,
  "data": {
    "id": "612342716134614477",
    "status": "success",
    "debugPort": 11019,
    "ipCheckPass": true
  }
}
```


## Request Example

```json
{
  "id": "612342716134614477",
  "webhook": "http://localhost:3001"
}
```


## Example response


```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "debugPort": 11001
  }
}
```


## Error Code

Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).


| Error Code | Description |
| --- | --- |
| -1 | Startup failed |
| 43007 | The environment is already in use |
| 43008 | The maximum number of open environments has been reached |
| 46003 | The environment is not included in the plan |
| 43028 | The sub-user does not have permissions for the environment group |
| 90002 | This environment does not exist. |
| 90003 | Insufficient disk space |

---

#### Close browser

[TOC]

## Interface Description

Used to close the corresponding browser. You need to specify the environment ID.


## Request URL

- `http://localhost:40185/api/v1/browser/stop`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | browser id | 539893235657500146 |


## Request Example


```json
{
 "id": "539893235657500146"
}
```


## Example response


```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success"
}
```


## Error Code


Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

| Error Code | Description |
| --- | --- |
| -1 | Shutdown failed |
| 43028 | The sub-user does not have permissions for this environment group |

---

#### Transfer browsers

[TOC]

## Interface Description

Transfer the browser to another team.


## Request URL

- `http://localhost:40185/api/v1/browser/transfer`


## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| username | yes | string | Target user account | Anna@geelark.com |
| envIds | yes | array[string] | Environment IDs to transfer. The maximum length of the array is 200. Entries exceeding 200 will be ignored. |["539893235657500146"]|
| transferOption | no | array[string] | Optional transfer option parameters: name: environment name, proxy: proxy, tag: tag, remark: remark, files: files | [ "name","proxy", "tag","remark" ] |


## Request Example


```json
{
  "envIds": ["539893235657500146"],
  "username": "Anna@geelark.com"
}
```


## Example response


```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
		"successCount": 10,
		"failCount": 2,
		"failEnvIds": ["539893235657500146"]
    }
}
```


## Response body data description


| Parameter Name | Type | Description |
| --- | --- | --- |
| successCount | integer | Number of successful transfers |
| failCount | integer | Number of failed transfers |
| failEnvIds | array[string] | IDs of environments where transfers failed, including those in use or non-existent environments |


## Error Code


Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).


| Error Code | Description |
| --- | --- |
| 40013 | Target user account does not exist |
| 43022 | Cannot transfer to own account |
| 43027 | This browser cannot be transferred |
| 40011 | The current user is not a paying user |
| 43028 | The sub-user does not have permissions for this environment group |

---

#### Check API interface status

[TOC]

## Interface Description

Used to check the availability of the current device's API interface.

## Request URL

- `http://localhost:40185/api/v1/status`

## Request Method

- POST

## Response Example

```json

{
"code": 0,

"msg": "success"

}```

## Error Codes

Please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

---

#### Check browser status

[TOC]

## API Description

Used to check the startup status of a specified browser. You need to specify the environment ID.

## Request URL

- `http://localhost:40185/api/v1/browser/status`

## Request Method

- POST

## Request Parameters

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Browser ID | 539893235657500146 |

## Request Example

```json
{
"id": "539893235657500146"
}
```

## Response Example

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "status": "open", // Browser is running "open", if not running it is "close"
    "debugPort": 11000
  }
}
```

## Error Codes

For error codes, please refer to [API Call Instructions](https://open.geelark.cn/api/request-instructions)

---

#### Clear browser cache

[TOC]

## API Description

Clears the local cache of the specified browser environment. For data security, please ensure this API is used when the browser environment is not open. If the disk space is insufficient, this API can be used to clear the cache to free up space.

## Request URL

- `http://localhost:40185/api/v1/browser/deleteCache`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Example | Description |
| --- | --- | --- | --- | --- |
| ids | Yes | array[string] | ["123456789","987654321"] | Browser ID |
| type | Yes | array[string] | ["local_storage","indexeddb"] | Types of cache to clear. Supported types: local_storage, indexeddb, extension_cache, cookie, history, image_file. |

## Request Example

```json
{
    "ids": [
        "123456789",
        "987654321"
    ],
    "type": [
        "local_storage",
        "indexeddb",
        "extension_cache",
        "cookie",
        "history",
        "image_file"
    ]
}
```

## Response Example

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "success_count": 2,
        "error_count": 0,
        "error_info": []
    }
}
```

## Error Codes

For error codes, please refer to the [API Call Instructions](https://open.geelark.cn/api/request-instructions)

---

#### Browser Mobile Grouping

[TOC]

## Interface description

Used to regroup environments and assign them to corresponding groups by ID.

## Request URL

- `http://localhost:40185/api/v1/browser/moveGroup`

## Request Method

- POST

## Request parameters

| Parameter name | Must be selected | Type | Example | Description
| --- | --- | --- | --- | --- |
| envIds | Yes | array[string] | ["123456789","987654321"] | browser IDs, up to 100 |
| groupId | Yes | string | "123456789" | group ID, and "0" is moved to ungrouped |

## Request example

```json
{
    "envIds":["123456789","987654321"],
    "groupId":"0"
}
```

## Response examples

```json
{
"traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
}
```

---

#### Query environment cookies

[TOC]

## API Description

Query and return the cookies of a specified environment. Only one environment can be queried at a time.


## Request URL

- `http://localhost:40185/api/v1/browser/getCookie`

## Request Method


- POST






## Request Parameters


| Parameter | Required | Type | Example | Description
| --- | --- | --- | --- | --- |
| id | Yes | string | "123456789" | Browser ID |


## Request Example


```json
{
    "id": "123456789"
}
```


## Response Example


```json
{
"traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success",
    "data": {
        "cookies": "[]"
    }
}
```

---

#### Set browser bookmarks

[TOC]


## API Description


Set browser bookmarks, and the bookmarks will be applied automatically when the browser environment starts.



## Request URL


- `http://localhost:40185/api/v1/browser/setBookmark`


## Request Method


- POST


## Request Parameters



| Parameter | Required | Type | Example | Description
| --- | --- | --- | --- | --- |
| browserBookmark | Yes | BrowserBookmark | Reference Request Example | Browser Bookmark |


### BrowserBookmark


| Parameter | Required | Type | Example | Description
| --- | --- | --- | --- | --- |
|type|Yes|integer|2|Bookmark type, 0-Not set, 1-Upload file, 2-Manually create|
|fileAddr|No|string|https://storage.com/bookmark.html|Bookmark HTML file address|
|text|No|string|Refer to request example|Manually create bookmark content, multiple bookmarks are separated by newline characters \n, supported formats:</br>Folder::Name::URL</br>Name::URL</br>URL|



## Request Example



```json
{
    "browserBookmark": {
        "type": 2,
        "fileAddr": "",
        "text": "http://a.com\nhttp://b.com"
    }
}
```



## Response Example



```json
{
    "traceId": "123456ABCDEF",
    "code": 0,
    "msg": "success"
}
```

---

#### Get browser bookmarks

[TOC]


## API Description


Querying browser bookmark settings does not require sending a request body.



## Request URL


- `http://localhost:40185/api/v1/browser/getBookmark`


## Request Method


- POST


## Response body data description


| Parameter Name | Type | Description |
| --- | --- | --- |
| browserBookmark | BrowserBookmark | Browser Bookmarks |


### BrowserBookmark


| Parameter Name | Type | Description |
| --- | --- | --- |
|type|integer|Bookmark type, 0 - No setting, 1 - Uploaded file, 2 - Manually created|
|fileAddr|string|Bookmark HTML file address|
|text|string|Manually created bookmark content, multiple bookmarks separated by newline characters \n, supported formats:</br>Folder::Name::URL</br>Name::URL</br>URL|



## Response Example



```json
{
    "traceId":"123456ABCDEF",
    "code":0,
    "msg":"success",
    "data":{
        "browserBookmark":{
            "type":2,
            "fileAddr":"",
            "text":"http://a.com\nhttp://b.com"
        }
    }
}
```

---

#### Clone browser

[TOC]

## API Description

- Generate a brand new browser with the same operating system and advanced settings

## Request URL

- `http://localhost:40185/api/v1/browser/clone`


## Request Method
- POST

## Request Parameters

| Parameter Name | Required | Type | Description |
| --- | --- | --- | --- |
|envId|Yes|string|Browser ID to clone|
|amount|Yes|integer|Number of clones, range 1-100|
|groupId|No|string|Target group ID, if not specified, it will be placed in an ungrouped group|
|cloneName|No|bool|Whether to clone the name|
|cloneRemark|No|bool|Whether to clone the remark|
|cloneTag|No|bool|Whether to clone the tag|
|cloneProxy|No|bool|Whether to clone the proxy|
|cloneCookie|No|bool|Whether to clone the cookie|
|cloneAccount|No|bool|Whether to clone the account information|

## Request Example
```json
{
    "envId": "590711571886417452",
	"amount": 1,
    "groupId": "590711571886417453"
}
```

## Response Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
| ids | array[string] |cloned browser ID|


## Response Example

```json
{
    "traceId": "B3DAFF64A7BD493CB1169D94A22BFC8D",
    "code": 0,
    "msg": "success",
    "data": {
        "ids": [
            "590711571886417454"
        ]
    }
}
```

---

#### Browser API / Automation / Task Management

##### Query task

[TOC]

## Interface Description

Get browser task list

## Request URL

- `http://localhost:40185/api/v1/browser/task/search`


## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | No | integer | Page number, defaults to 1 if not specified | 1 |
| pageSize | No | integer | Page size, maximum 100, defaults to 10 if not specified | 10 |
| taskIds | No | array[string] | Task ID | Refer to request example |


## Request Example

```json
{
    "page": 1,
	"pageSize": 10,
    "taskIds": ["497652752864775437"]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
|total|integer|Total number of data|
|page|integer|Page number|
|pageSize|integer|Page size|
|list|array[Task]|Data list|

### Task

| Parameter Name | Type | Description |
| --- | --- | --- |
|id|string|Task ID|
|eid|string|Environment ID|
|name|string|Task Name|
|remark|string|Task Remark|
|serialName|string|Environment Name|
|status|integer|Task Status, 1-Waiting for Execution 2-Executing 3-Task Completed 4-Task Failed 7-Task Cancelled|
|startAt|integer|Start Time, Second-level Timestamp|
|finishAt|integer|End Time, Second-level Timestamp|
|cost|integer|Time Elapsed in Seconds|
|resultCode|integer|Task Result Code, Refer to Task Failure Code and Reason|
|resultDesc|string|Task Result Description, Refer to Task Failure Code and Reason|
|scheduleAt|integer|Task Scheduled Execution Time, Second-level Timestamp|

### Task Failure Codes and Reasons

| Failure Code | Failure Reason |
| - | - |
|20001|The task started earlier than the current time|
|20002|Browser failed to start|
|29999|The task was interrupted|

## Example response

```json
{
	"traceId":"2XsBK1HDR",
	"code":0,
	"msg":"success",
	"data":{
		"total":1,
		"page":1,
		"pageSize":10,
		"list":[
			{
				"id":"497652752864775437",
				"eid":"497652752864775438",
				"name":"myTask",
				"remark":"",
				"serialName":"",
				"status":3,
				"startAt":1762912197,
				"finishAt":1762912497,
				"cost":300,
				"resultCode":0,
				"resultDesc":"success",
				"scheduleAt":1762912197
			}
		]
	}
}
```


## Error Code


Please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

---

##### Cancel task

[TOC]


## Interface Description

Cancel the browser task; you can cancel it while it's running or waiting to be executed.

## Request URL

- `http://localhost:40185/api/v1/browser/task/cancel`

## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string| task id |497652752864775437 |



## Request Example

```json
{
    "taskId": "497652752864775437"
}
```


## Example response

```json
{
	"traceId":"2XsBK1HDR",
	"code":0,
	"msg":"success"
}
```

## Error Code



Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).


| Error Code | Description |
| --- | --- |
|48001|Task status does not allow operation|
|48005|Only the creator is allowed to operate|

---

##### Retry Task

[TOC]


## Interface Description

Retry the browser task; you can retry if the task fails or is canceled.

## Request URL

- `http://localhost:40185/api/v1/browser/task/restart`

## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| taskId | Yes | string| task id |497652752864775437 |


## Request Example

```json
{
    "taskId": "497652752864775437"
}
```


## Example response

```json
{
	"traceId":"2XsBK1HDR",
	"code":0,
	"msg":"success"
}
```

## Error Code



Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).


| Error Code | Description |
| --- | --- |
|48001|Task status does not allow operation|
|48005|Only the creator is allowed to operate|

---

##### Query task details

[TOC]

## Interface Description

Get Browser Task Details

## Request URL

- `http://localhost:40185/api/v1/browser/task/detail`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| ----------- | -------| -----------|----------- |----------- |
| taskId | Yes | string | Task ID | 497652752864775437 |


## Request Example

```json
{
    "taskId": "497652752864775437"
}
```

## Response Body Data Description

| Parameter Name | Type | Description |
| ----------- | -----------|----------- |
|id|string|Task ID|
|eid|string|Environment ID|
|name|string|Task Name|
|remark|string|Task Remark|
|serialName|string|Environment Name|
|status|integer|Task Status, 1-Waiting for Execution 2-Executing 3-Task Completed 4-Task Failed 7-Task Cancellation |
|startAt|integer|Start time, timestamp in seconds|
|finishAt|integer|End time, timestamp in seconds|
|cost|integer|Time elapsed in seconds|
|resultCode|integer|Task result code, refer to task failure codes and reasons|
|resultDesc|string|Task result description, refer to task failure codes and reasons|
|scheduleAt|integer|Task scheduled execution time, timestamp in seconds|
|logs|array[string]|Task logs|

### Task Failure Codes and Reasons

| Failure Code | Failure Reason |
| - | - |
|20001|Task start time is earlier than current time|
|20002|Browser failed to start|
|29999|Task was interrupted|

## Response Example

```json
{
	"traceId":"2XsBK1HDR",
	"code":0,
	"msg":"success",
	"data":{
		"id":"609019758523737585",
		"eid":"600729455865921210",
		"name":"task20260303182734",
		"remark":"",
		"serialName":"",
		"status":3,
		"startAt":1772533706,
		"finishAt":1772533707,
		"cost":1,
		"resultCode":0,
		"resultDesc":"success",
		"scheduleAt":1772533659,
		"logs":["[2026-03-03 10:28:26 118] New Tab:"]
	}
}
```

---

#### Browser API / Automation / TikTok

##### TikTok search videos, likes and comments

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/tiktokSearch`

## Request method

- POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|searchKeyword|Yes|string|search keyword|hello|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"searchKeyword": "hello"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok like and comment on videos

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/tiktokComment`

## Request method

- POST

## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|comments| Yes |array[string]|comments|reference request example|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"comments": ["hello"]
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### TikTok like specified videos

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/tiktokLike`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|videoLink|Yes|string|Video link|https://www.tiktok.com/video/38210380122|
|comment|No|string|Comment|hello|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"videoLink": "https://www.tiktok.com/video/38210380122",
	"comment": "hello"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / Facebook

##### Facebook Post a Status

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/facebookPost`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|content|Yes|string|Content|hello|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"content": "hello"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook add recommended friends

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/facebookFriends`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook like all on the first screen

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/facebookLike`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Facebook account creates a homepage

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/facebookHomepage`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|mainPageName| Yes | string| Homepage name data | myPage|
| category| Yes | array[string]| Homepage category data | Refer to request example|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"mainPageName": "myPage",
	"category": ["dev"]
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / Instagram

##### Browse and like Instagram feed

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/instagramLike`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### Instagram search hashtags and browse posts

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/instagramSearch`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|searchKeywords|Yes|array[string]|Search keywords|refer to request example|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"searchKeywords": ["hello"]
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / YouTube

##### YouTube Watch Videos

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/youtubeWatch`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|searchKeyword| Yes |string|search keyword|hello|
|title| Yes |string|title|myTitle|
|comment| Yes |string|comment|myComment|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"searchKeyword": "hello",
	"title": "myTitle",
	"comment": "myComment"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / X(Twitter)

##### X(Twitter) Retweet and Post a Tweet

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/xPost`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|content|Yes|string|Content|hello|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"content": "hello"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

##### X(Twitter) like and retweet tweets

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/xLike`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390"
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / Reddit

##### Browse and like Reddit posts searched by keywords

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/redditLike`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|searchKeywords|Yes|array[string]|Search keywords | Reference request example |


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"searchKeywords": ["hello"]
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

#### Browser API / Automation / Custom Task

##### Task flow query

[TOC]


## Interface Description

Get browser custom task flow list

## Request URL

- `http://localhost:40185/api/v1/browser/task/flow`

## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | No | integer | Page number, defaults to 1 if not specified | 1 |
| pageSize | No | integer | Page size, maximum 100, defaults to 10 if not specified | 10 |



## Request Example

```json
{
    "page": 1,
	"pageSize": 10
}
```

## Response Data Description


| Parameter Name | Type | Description |
| --- | --- | --- |
|total|integer|Total number of data points|
|page|integer|Page number|
|pageSize|integer|Page size|
|list|array[Flow]|List of data points|

### Flow

| Parameter Name | Type | Description |
| --- | --- | --- |
|id|string|Task Flow ID|
|title|string|Task Flow Title|
|desc|string|Task Flow Remarks|
|params|array[string]|Task Flow Parameter Field Names|

## Example response

```json
{
	"traceId":"2XsBK1HDR",
	"code":0,
	"msg":"success",
	"data":{
		"total":1,
		"page":1,
		"pageSize":10,
		"list":[
			{
				"id":"497652752864775437",
				"title": "video flow",
				"desc": "this is a video flow",
				"params": ["Title","Desc"]
			}
		]
	}
}
```

## Error Code



Please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).

---

##### Create custom task

[TOC]


## Interface Description

First, call the custom process query interface to obtain the browser's custom task process, and then create the task using the process ID.

## Request URL

- `http://localhost:40185/api/v1/browser/task/add`

## Request method



- POST



## Request Parameters



| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|flowId|Yes|string|Task flow ID, the ID field returned by the task flow query interface|497652752864775437|
|paramMap|No|object|Task flow parameters, with corresponding parameter types as follows:<br>String: string<br>Batch text: array[string]<br>Number: number<br>Boolean: bool<br>File: array[string]|Refer to request example|


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
    "flowId": "562316072435344885",
    "paramMap": {
        "Title": "video",
        "Desc": "this is video",
        "Video": ["https://material.geelark.cn/a.mp4"]
    }
}
```


## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

## Error Code



Below are specific error codes for this interface. For other error codes, please refer to [Browser Error Codes](https://open.geelark.com/api/browser-error-codes).


| Error Code | Description |
| --- | --- |
|43028|User does not have permission for this environment group|
|43027|Environment not supported|
|46002|Package expired, member unavailable|
|46003|Package expired, environment unavailable|

---

#### Browser API / Automation / Other Task

##### Cookie Bot

[TOC]

## Request URL

- `http://localhost:40185/api/v1/browser/task/cookieBot`

## Request method


- POST


## Request Parameters


| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
|eid|Yes|string|Environment ID|497652752864775437|
|name|No|string|Task name, maximum 128 characters|myTask|
|remark|No|string|Remark, maximum 200 characters|myRemark|
|scheduleAt|Yes|integer|Schedule time, second-level timestamp|1741846843|
|pages|Yes|array[string]|The webpage to be accessed | Refer to the request example |


## Request Example

```json
{
    "name":"test",
    "remark":"test remark",
    "scheduleAt": 1741846843,
    "eid":"557536075321468390",
	"pages": ["https://a.com"]
}
```

## Example response

```json
{
    "traceId": "A4D8BCF69B878A71AC589F5CB1D80EAB",
    "code": 0,
    "msg": "success",
    "data": {
        "taskId": "558017255909123564"
    }
}
```

---

## Proxy Management

### Add proxy

[TOC]

## API Description

Duplicate proxies will not be added.

## Request URL

- `https://openapi.geelark.com/open/v1/proxy/add`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| list | Yes | array[ProxyAddItem] | The list of proxy information items can contain up to 100 entries. | Reference request example |

### ProxyAddItem proxy information items

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| scheme | Yes | string | Proxy types，socks5，http，https | socks5 |
| server | Yes | string | Proxy address | 192.3.8.1 |
| port | Yes | integer | Proxy port | 8000 |
| username | No | string | Proxy username | admin |
| password | No | string | Proxy password | admin |
| proxyQueryChannel | No | integer | Detection channels: 1. IPApi; 2. IP2Location; default is IP2Location | 2 |


## Request Examples

```json
{
	"list": [
		{
			"scheme": "socks5",
			"server": "192.3.8.1",
			"port": 8000,
			"username": "admin",
			"password": "admin",
			"proxyQueryChannel" : 1
		}
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total processed, the same as the number of proxy information items provided. |
| successAmount | integer | Number of successful additions |
| failAmount | integer | Number of failed additions |
| failDetails | array[FailDetail] | Failed proxy information |
| successDetails | array[SuccessDetail] | Successful proxy information |

### FailDetail Failed proxy information

| Parameter Name | Type | Description |
| --- | --- | --- |
| index | integer | Index of the provided proxy information items |
| code | integer | Error code, refer to failure code and message |
| msg| string | Error message, refer to failure code and message |

### SuccessDetail Successful proxy information

| Parameter Name | Type | Description |
| --- | --- | --- |
| index | integer | Index of the provided proxy information items |
| id | string | Proxy ID; if the provided proxy information items are the same, the proxy ID will be the same. |

### Failure code and message

| code | msg |
| - | - |
| 40000 | unknown error |
| 45003 | proxy not allow |
| 45004 | check proxy failed |
| 45007 | proxy already exists |

## Response Example

```json
{
    "traceId": "31ec87cd-b8a0-40c1-984e-9d6b8a483322",
    "code": 40006,
    "msg": "partial success",
    "data": {
		"totalAmount": 2,
		"successAmount": 1,
		"failAmount": 1,
		"failDetails": [
			{
				"index": 0,
				"code": 45007,
				"msg": "proxy already exists"
			}
		],
		"successDetails": [
			{
				"index": 1,
				"id": "493188072704313353"
			}
		]
	}
}
```
## Error Codes

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Update proxy

[TOC]

## API Description

Update proxy

## Request URL

- `https://openapi.geelark.com/open/v1/proxy/update`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| list | Yes | array[ProxyUpdateItem] | The list of proxy information items can contain up to 100 entries. | Reference request example |

### ProxyUpdateItem proxy information items

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| id | Yes | string | Proxy ID | 493188072704313353 |
| scheme | Yes | string | Proxy types，socks5，http，https | socks5 |
| server | Yes | string | Proxy address | 192.3.8.1 |
| port | Yes | integer | Proxy port | 8000 |
| username | No | string | Proxy username | admin |
| password | No | string | Proxy password | admin |
| proxyQueryChannel | No | integer | Detection channels: 1 IPApi; 2 IP2Location; default to original detection channel | 2 |


## Request Examples

```json
{
	"list": [
		{
			"id": "493188072704313353",
			"scheme": "socks5",
			"server": "192.3.8.1",
			"port": 8000,
			"username": "admin",
			"password": "admin",
			"proxyQueryChannel" : 1
		}
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total processed, duplicate IDs provided will not be counted. |
| successAmount | integer | Number of successfully processed items |
| failAmount | integer | Number of failed items |
| failDetails | array[FailDetail] | Failed proxy information |

### FailDetail Failed proxy information

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Proxy ID |
| code | integer | Error code, refer to failure code and message |
| msg| string | Error message, refer to failure code and message |

### Failure code and message

| code | msg |
| - | - |
| 40005 | proxy not found |
| 40000 | unknown error |
| 45003 | proxy not allow |
| 45004 | check proxy failed |
| 45007 | proxy already exists |
| 45008 | proxy type not allow |

## Response Example

```json
{
    "traceId": "31ec87cd-b8a0-40c1-984e-9d6b8a483322",
    "code": 40006,
    "msg": "partial success",
    "data": {
		"totalAmount": 2,
		"successAmount": 1,
		"failAmount": 1,
		"failDetails": [
			{
				"id": "493188072704313353",
				"code": 40005,
				"msg": "proxy not found"
			}
		]
	}
}
```
## Error Codes

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Delete proxy

[TOC]

## API Description

Delete proxy

## Request URL

- `https://openapi.geelark.com/open/v1/proxy/delete`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| ids | Yes | array[string] | Proxy ID list, up to 100 IDs. | Reference request example |

## Request Examples

```json
{
	"ids": [
		"493188072704313353"
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| totalAmount | integer | Total processed, duplicate IDs provided will not be counted. |
| successAmount | integer | Number of successfully processed items |
| failAmount | integer | Number of failed items |
| failDetails | array[FailDetail] | Failed proxy information |

### FailDetail Failed proxy information

| Parameter Name | Type | Description |
| id | string | Proxy ID |
| code | integer | Error code, refer to failure code and message |
| msg| string | Error message, refer to failure code and message |

### Failure code and message

| code | msg |
| - | - |
| 40005 | proxy not found |
| 40010 | proxy binds to the environment |

## Response Example

```json
{
    "traceId": "31ec87cd-b8a0-40c1-984e-9d6b8a483322",
    "code": 40006,
    "msg": "partial success",
    "data": {
		"totalAmount": 2,
		"successAmount": 1,
		"failAmount": 1,
		"failDetails": [
			{
				"id": "493188072704313353",
				"code": 40005,
				"msg": "proxy not found"
			}
		]
	}
}
```
## Error Codes

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Get all proxies

[TOC]

## API Description

Get all proxies

## Request URL

- `https://openapi.geelark.com/open/v1/proxy/list`

## Request Method

*   POST

## Request Parameters

| Parameter Name | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| page | Yes | integer | Page number, minimum value is 1. | 1 |
| pageSize | Yes | integer | Number of items per page, minimum is 1, maximum is 100. | 1 |
| ids | No | array[string] | Proxy ID list | Reference request example |

## Request Examples

```json
{
	"page": 1,
	"pageSize": 1,
	"ids": [
		"493188072704313353"
	]
}
```

## Response Data Description

| Parameter Name | Type | Description |
| --- | --- | --- |
| total | integer | Total number of items |
| page | integer | Page number |
| pageSize | integer | Number of items per page |
| list | array[ProxyListItem] | The list of proxy information items |

### ProxyListItem 代理信息项

| Parameter Name | Type | Description |
| --- | --- | --- |
| id | string | Proxy ID |
| serialNo | integer | Proxy serial number |
| scheme | string | Proxy types，socks5，http，https |
| server | string | Proxy address |
| port | integer | Proxy port |
| username | string | Proxy username |
| password | string | Proxy password |

## Response Example

```json
{
    "traceId": "31ec87cd-b8a0-40c1-984e-9d6b8a483322",
    "code": 0,
    "msg": "success",
    "data": {
		"total": 1,
		"page": 1,
		"pageSize": 1,
		"list": [
			{
				"id": "493188072704313353",
				"serialNo": 1,
				"scheme": "socks5",
				"server": "192.3.8.1",
				"port": 8000,
				"username": "admin",
				"password": "admin"
			}
		]
	}
}
```
## Error Codes

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

---

### Proxy Detection

[TOC]

API Description
---------------

Proxy Detection API

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/proxy/check`
    

Request Method
--------------

*   POST
    

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| --- | --- | --- | --- | --- |
| proxyQueryChannel | Yes | string | IP lookup source, supports only `IP-API` or `IP2Location` | IP2Location |
| proxyType | Yes | string | Proxy type, supports only `socks5`, `http`, or `https` | socks5 |
| server | Yes | string | Host | 185.162.130.86 |
| port | Yes | integer | Port number | 11000 |
| username | No | string | Proxy username | username |
| password | No | string | Proxy password | pass |

Request Example
---------------
```json
{
	"proxyQueryChannel": "IP2Location",
	"proxyType": "socks5",
	"server": "185.162.130.86",
	"port": 10000,
	"username": "username",
	"password": "pass"
}
```

Response Data Description
-------------------------

| Field | Type | Description |
| --- | --- | --- |
| detectStatus | bool | Whether the detection was successful |
| message | string | Reason for failure (if any) |
| outboundIP | string | Outbound IP |
| countryCode | string | Country code of the outbound IP |
| countryName | string | Country name of the outbound IP |
| subdivision | string | State/Province of the outbound IP |
| city | string | City of the outbound IP |
| timezone | string | Time zone of the outbound IP |
| isp | string | ISP of the outbound IP |

Response Example
----------------
```json
{
	"traceId": "B379AA1BBBB529758ED091C480AA4285",
	"code": 0,
	"msg": "success",
	"data": {
		"detectStatus": true,
		"message": "",
		"outboundIP": "223.135.25.196",
		"countryCode": "JP",
		"countryName": "Japan",
		"subdivision": "Tokyo",
		"city": "Tokyo",
		"timezone": "Asia/Tokyo",
		"isp": "Sony Network Communications Inc."
	}
}
```

Error Codes
-----------

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

## Tag Management

### Create tag

[TOC]

## Interface Description

- Create tags with specified **name and color (optional)**.
- Support batch creation.
- If no color is selected during creation, the default color is **white**.

### Color List

- `white`
- `red`
- `blue`
- `green`
- `yellow`
- `purple`

## Request URL

- `https://openapi.geelark.com/open/v1/tag/add`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description       | Example           |
| -------------- | -------- | ------------- | ----------------- | ----------------- |
| list           | Yes      | array[TagItem] | Tag data list     | Refer to Request Example |

### list Data List <TagItem>

| Parameter Name | Required | Type   | Description | Example                   |
| -------------- | -------- | ------ | ----------- | ------------------------- |
| name           | Yes      | string | Tag name, up to 30 characters    | tag                       |
| color          | No       | string | Tag color   | white, see color list for details |

## Request Example

```json
{
  "list": [
    {
      "name": "tagEmpty"
    },
    {
      "name": "tagRed",
      "color": "red"
    },
    {
      "name": "tagBlue",
      "color": "blue"
    },
    {
      "name": "tagGreen",
      "color": "green"
    },
    {
      "name": "tagYellow",
      "color": "yellow"
    },
    {
      "name": "tagPurple",
      "color": "purple"
    },
    {
      "name": "tagWhite",
      "color": "white"
    },
    {
      "name": "tagWhite2",
      "color": ""
    },
    {
      "name": "tagInvalid",
      "color": "abc"
    }
  ]
}
```

## Response Example

```json
{
  "traceId": "BC78266DA98F18EA9278B9C89AF9BB9B",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 9,
    "successAmount": 8,
    "failAmount": 1,
    "successDetails": [
      {
        "id": "528989565877224448",
        "name": "tagWhite2",
        "color": "white"
      },
      {
        "id": "528989565877289984",
        "name": "tagBlue",
        "color": "blue"
      },
      {
        "id": "528989565877355520",
        "name": "tagGreen",
        "color": "green"
      },
      {
        "id": "528989565894001664",
        "name": "tagYellow",
        "color": "yellow"
      },
      {
        "id": "528989565894067200",
        "name": "tagPurple",
        "color": "purple"
      },
      {
        "id": "528989565894132736",
        "name": "tagWhite",
        "color": "white"
      },
      {
        "id": "528989565894198272",
        "name": "tagEmpty",
        "color": "white"
      },
      {
        "id": "528989565910778880",
        "name": "tagRed",
        "color": "red"
      }
    ],
    "failDetails": [
      {
        "code": 43023,
        "name": "tagInvalid",
        "msg": "tag color not found"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type               | Description          |
| -------------- | ------------------ | -------------------- |
| totalAmount    | integer            | Total requests       |
| successAmount  | integer            | Total successes      |
| failAmount     | integer            | Total failures       |
| successDetails | array[SuccessDetails] | Success details      |
| failDetails    | array[FailDetails]   | Failure details      |

### successDetails Success Info <SuccessDetails>

| Parameter Name | Type   | Description |
| -------------- | ------ | ----------- |
| id             | string | Tag ID      |
| name           | string | Tag name    |
| color          | string | Tag color   |

### failDetails Failure Info <FailDetails>

| Parameter Name | Type    | Description |
| -------------- | ------- | ----------- |
| code           | integer | Error code  |
| name           | string  | Tag name    |
| msg            | string  | Error msg   |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43020      | Tag name is empty                  |
| 43021      | Tag name already exists            |
| 43023      | Tag color not supported, see color list |

---

### Delete tag

[TOC]


## Interface Description

- Delete the corresponding tags.

## Request URL

- `https://openapi.geelark.com/open/v1/tag/delete`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description           | Example           |
| -------------- | -------- | ------------- | --------------------- | ----------------- |
| ids            | Yes      | array[string] | List of tag IDs to delete | Refer to Request Example |

## Request Example

```json
{
  "ids": ["528989565877224448", "528953724308030464"]
}
```

## Response Example

```json
{
  "traceId": "ACEB0CFEB887F99CB989BC9D9FF92BBC",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 2,
    "successAmount": 1,
    "failAmount": 1,
    "failDetails": [
      {
        "code": 43022,
        "id": "528953724308030464",
        "msg": "tag not found"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| -------------- | ----------------- | -------------------- |
| totalAmount    | integer           | Total delete requests |
| successAmount  | integer           | Total successes      |
| failAmount     | integer           | Total failures       |
| failDetails    | array[FailDetails] | Failure details      |

### failDetails Failure Info <FailDetails>

| Parameter Name | Type    | Description |
| -------------- | ------- | ----------- |
| code           | integer | Error code  |
| id             | string  | Tag ID      |
| msg            | string  | Error msg   |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43022      | Tag does not exist                 |

---

### Query tag

[TOC]


## Interface Description

- Retrieve tag information.

**Refer to the Create Tag API for the list of tag colors.**

## Request URL

- `https://openapi.geelark.com/open/v1/tag/list`

## Request Method

- POST

## Request Parameters

### Pagination Parameters

| Parameter Name | Required | Type    | Description                                      | Example |
| -------------- | -------- | ------- | ------------------------------------------------ | ------- |
| page           | Yes      | integer | Page number, minimum is 1                        | 1       |
| pageSize       | Yes      | integer | Number of items per page, minimum is 1, maximum is 100 | 10      |

### Query Parameters

| Parameter Name | Required | Type          | Description       | Example           |
| -------------- | -------- | ------------- | ----------------- | ----------------- |
| ids            | No       | array[string] | List of tag IDs   | Refer to Request Example |
| names          | No       | array[string] | List of tag names | Refer to Request Example |
| colors         | No       | array[string] | List of tag colors| Refer to Request Example |

## Request Example

### Without Query Conditions

```json
{
  "page": 1,
  "pageSize": 5
}
```

### Query by IDs

```json
{
  "page": 1,
  "pageSize": 5,
  "ids": ["528989565910778880", "528989565894198272"]
}
```

### Query by Names

```json
{
  "page": 1,
  "pageSize": 5,
  "names": ["tagRed", "tagWhite"]
}
```

### Query by Colors

```json
{
  "page": 1,
  "pageSize": 5,
  "colors": ["blue", "red"]
}
```

## Response Example

```json
{
  "traceId": "913AE8DBBBB48B70825EBAABB11B91BD",
  "code": 0,
  "msg": "success",
  "data": {
    "total": 24,
    "page": 1,
    "pageSize": 5,
    "list": [
      {
        "id": "528989565877355520",
        "name": "tagGreen",
        "color": "green"
      },
      {
        "id": "528989565877289984",
        "name": "tagBlue",
        "color": "blue"
      },
      {
        "id": "528989565894067200",
        "name": "tagPurple",
        "color": "purple"
      },
      {
        "id": "528989565910778880",
        "name": "tagRed",
        "color": "red"
      },
      {
        "id": "528989565894198272",
        "name": "tagEmpty",
        "color": "white"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| -------------- | ----------------- | -------------------- |
| total          | integer           | Total count          |
| page           | integer           | Page number          |
| pageSize       | integer           | Page size            |
| list           | array[Tag]        | Tag list             |
| failDetails    | array[FailDetail] | Failure details      |

### list Tag List <Tag>

| Parameter Name | Type   | Description |
| -------------- | ------ | ----------- |
| id             | string | Tag ID      |
| name           | string | Tag name    |
| color          | string | Tag color   |

### failDetails Failure Info <FailDetail>

| Parameter Name | Type    | Description                                      |
| -------------- | ------- | ------------------------------------------------ |
| code           | integer | Error code                                       |
| type           | integer | Failure type: 1-Tag ID, 2-Tag name, 3-Tag color  |
| param          | string  | Failed parameter                                 |
| msg            | string  | Failure message                                  |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43022      | Tag does not exist                 |
| 43023      | Tag color does not exist           |
| 43024      | Tag name does not exist            |

---

### Modify tag

[TOC]


## Interface Description

- Modify tag information including name and color.

**Refer to the Create Tag API for the list of tag colors.**

## Request URL

- `https://openapi.geelark.com/open/v1/tag/update`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type       | Description           | Example           |
| -------------- | -------- | ---------- | --------------------- | ----------------- |
| list           | Yes      | array[Tag] | Array of tags to update | Refer to Request Example |

### list Modify Tag Array <Tag>

| Parameter Name | Required | Type   | Description | Example           |
| -------------- | -------- | ------ | ----------- | ----------------- |
| id             | Yes      | string | Tag ID      | Refer to Request Example |
| name           | No       | string | New tag name, up to 30 characters| Refer to Request Example |
| color          | No       | string | New tag color| Refer to Request Example |

- If the tag information includes a name, it cannot be an empty string.

## Request Example

```json
{
  "list": [
    {
      "id": "528989565894198272",
      "name": "tagEmptyUpdate",
      "color": "red"
    },
    {
      "id": "528994200482481152",
      "name": "tagUpdate",
      "color": "red"
    }
  ]
}
```

## Response Example

```json
{
  "traceId": "B178151A9586E88195C4BF1493BBC98B",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 2,
    "successAmount": 2,
    "failAmount": 0
  }
}
```

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43020      | Tag name is empty                  |
| 43022      | Tag does not exist                 |
| 43023      | Tag color not supported            |

---

## Group Management

### Create group

[TOC]


## Interface Description

- Create groups with specified **name and remark (optional)**.
- Support batch creation.

## Request URL

- `https://openapi.geelark.com/open/v1/group/add`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type             | Description           | Example           |
| -------------- | -------- | ---------------- | --------------------- | ----------------- |
| list           | Yes      | array[GroupItem] | Group data list       | Refer to Request Example |

### list Data List <GroupItem>

| Parameter Name | Required | Type   | Description | Example |
| -------------- | -------- | ------ | ----------- | ------- |
| name           | Yes      | string | Group name, up to 50 characters  | tag     |
| remark         | No       | string | Group remark, up to 500 characters| remark  |

## Request Example

```json
{
  "list": [
    {
      "name": "group"
    },
    {
      "name": "groupRemark",
      "remark": "remark"
    },
    {
      "name": "groupInvalid"
    }
  ]
}
```

## Response Example

```json
{
  "traceId": "AA6849499B949BDCBD7FA792AB1981A5",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 3,
    "successAmount": 2,
    "failAmount": 1,
    "successDetails": [
      {
        "id": "528994851237135360",
        "name": "group"
      },
      {
        "id": "528994851237200896",
        "name": "groupRemark",
        "remark": "remark"
      }
    ],
    "failDetails": [
      {
        "code": 43031,
        "name": "groupInvalid",
        "msg": "group existed"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type               | Description          |
| -------------- | ------------------ | -------------------- |
| totalAmount    | integer            | Total requests       |
| successAmount  | integer            | Total successes      |
| failAmount     | integer            | Total failures       |
| successDetails | array[SuccessDetails] | Success details      |
| failDetails    | array[FailDetails]   | Failure details      |

### successDetails Success Info <SuccessDetails>

| Parameter Name | Type   | Description          |
| -------------- | ------ | -------------------- |
| id             | string | Group ID             |
| name           | string | Group name           |
| remark         | string | Remark (not shown if empty) |

### failDetails Failure Info <FailDetails>

| Parameter Name | Type    | Description |
| -------------- | ------- | ----------- |
| code           | integer | Error code  |
| name           | string  | Group name  |
| msg            | string  | Error msg   |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43030      | Group name is empty                |
| 43031      | Group name already exists          |

---

### Delete group

[TOC]

## Interface Description

- Delete the corresponding groups.

## Request URL

- `https://openapi.geelark.com/open/v1/group/delete`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type          | Description           | Example           |
| -------------- | -------- | ------------- | --------------------- | ----------------- |
| ids            | Yes      | array[string] | List of group IDs to delete | Refer to Request Example |

## Request Example

```json
{
  "ids": ["528994851237200896", "528994851237135360", "528984285433037824"]
}
```

## Response Example

```json
{
  "traceId": "AA69C5B4938EDB00920099719D58C8A9",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 3,
    "successAmount": 2,
    "failAmount": 1,
    "failDetails": [
      {
        "code": 43032,
        "id": "528984285433037824",
        "msg": "group not found"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| -------------- | ----------------- | -------------------- |
| totalAmount    | integer           | Total delete requests |
| successAmount  | integer           | Total successes      |
| failAmount     | integer           | Total failures       |
| failDetails    | array[FailDetails] | Failure details      |

### failDetails Failure Info <FailDetails>

| Parameter Name | Type    | Description |
| -------------- | ------- | ----------- |
| code           | integer | Error code  |
| id             | string  | Group ID    |
| msg            | string  | Error msg   |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43032      | Group does not exist               |
| 43035      | Operation not allowed on ungrouped |

---

### Query group

[TOC]


## Interface Description

- Retrieve group information.

## Request URL

- `https://openapi.geelark.com/open/v1/group/list`

## Request Method

- POST

## Request Parameters

### Pagination Parameters

| Parameter Name | Required | Type    | Description                                      | Example |
| -------------- | -------- | ------- | ------------------------------------------------ | ------- |
| page           | Yes      | integer | Page number, minimum is 1                        | 1       |
| pageSize       | Yes      | integer | Number of items per page, minimum is 1, maximum is 100 | 10      |

### Query Parameters

| Parameter Name | Required | Type          | Description       | Example           |
| -------------- | -------- | ------------- | ----------------- | ----------------- |
| ids            | No       | array[string] | List of group IDs | Refer to Request Example |
| names          | No       | array[string] | List of group names | Refer to Request Example |
| remarks        | No       | array[string] | List of group remarks | Refer to Request Example |

## Request Example

### Without Query Conditions

```json
{
  "page": 1,
  "pageSize": 5
}
```

### Query by IDs

```json
{
  "page": 1,
  "pageSize": 5,
  "ids": ["528995439832269824", "528985080069096448"]
}
```

### Query by Names

```json
{
  "page": 1,
  "pageSize": 5,
  "names": ["groupRemark", "testRemark"]
}
```

### Query by Remarks

```json
{
  "page": 1,
  "pageSize": 5,
  "remarks": ["remark", "test"]
}
```

## Response Example

```json
{
  "traceId": "A25B0025BA886B1EB2679AAAAC599998",
  "code": 0,
  "msg": "success",
  "data": {
    "total": 2,
    "page": 1,
    "pageSize": 5,
    "list": [
      {
        "id": "528995439832269824",
        "name": "groupRemark",
        "remark": "remark"
      },
      {
        "id": "528985080069096448",
        "name": "testRemark",
        "remark": "test"
      }
    ]
  }
}
```

## Response Data Description

| Parameter Name | Type              | Description          |
| -------------- | ----------------- | -------------------- |
| total          | integer           | Total count          |
| page           | integer           | Page number          |
| pageSize       | integer           | Page size            |
| list           | array[Group]      | Group list           |
| failDetails    | array[FailDetails] | Failure details      |

### list Group List <Group>

| Parameter Name | Type   | Description |
| -------------- | ------ | ----------- |
| id             | string | Group ID    |
| name           | string | Group name  |
| remark         | string | Group remark|

### failDetails Failure Info <FailDetails>

| Parameter Name | Type    | Description                                      |
| -------------- | ------- | ------------------------------------------------ |
| code           | integer | Error code                                       |
| type           | integer | Failure type: 1-Group ID, 2-Group name, 3-Group remark |
| param          | string  | Failed parameter                                 |
| msg            | string  | Failure message                                  |

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43032      | Group does not exist               |
| 43033      | Group name does not exist          |
| 43034      | Group remark does not exist        |

---

### Modify group

[TOC]

## Interface Description

- Modify group information including name and remark.

## Request URL

- `https://openapi.geelark.com/open/v1/group/update`

## Request Method

- POST

## Request Parameters

| Parameter Name | Required | Type       | Description           | Example           |
| -------------- | -------- | ---------- | --------------------- | ----------------- |
| list           | Yes      | array[Group] | Group data            | Refer to Request Example |

### list Group Data <Group>

| Parameter Name | Required | Type   | Description | Example           |
| -------------- | -------- | ------ | ----------- | ----------------- |
| id             | Yes      | string | Group ID    | Refer to Request Example |
| name           | No       | string | New group name, up to 50 characters| Refer to Request Example |
| remark         | No       | string | New group remark, up to 500 characters| Refer to Request Example |

- If `name` is provided, it cannot be an empty string.

## Request Example

```json
{
  "list": [
    {
      "id": "528995439832269824",
      "name": "newGroupRemark",
      "remark": "update remark"
    }
  ]
}
```

## Response Example

```json
{
  "traceId": "B068F85E849B683291AE8ECCBB7B3DB9",
  "code": 0,
  "msg": "success",
  "data": {
    "totalAmount": 1,
    "successAmount": 1,
    "failAmount": 0
  }
}
```

## Error Codes

Below are the specific error codes for this interface. For other error codes, please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes).

| Error Code | Description                        |
| ---------- | ---------------------------------- |
| 43030      | Group name is empty                |
| 43032      | Group does not exist               |
| 43035      | Operation not allowed on ungrouped |

---

## Billing

### Balance Inquiry

[TOC]

API Description
---------------

Query account balance, this API has a rate limit of 10 requests per minute.

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/pay/wallet`
    

Request Method
--------------

*   POST
    

Response Body Description
-------------------------

| Parameter | Type | Description |
| --- | --- | --- |
| balance | float | Balance |
| giftMoney | float | Gifted amount |
| availableTimeAddOn | integer   | Remaining time add-on |

Response Example
----------------


```json
{
	 "traceId": "9C798E6CA2AB58348E2C974EA8E8AB8B",
	"code": 0,
	 "msg": "success",
	 "data": {
		"balance": 1549.77,
		"giftMoney": 0,
		"availableTimeAddOn" : 10
	}
}
```

---

### Get plan list

[TOC]

API Description
---------------

Get all plan info

Request URL
-----------

- `https://openapi.geelark.com/open/v1/pay/profiles/list`

Request Method
--------------

- POST

Response Body Description
-------------------------

| Parameter | Type | Description |
| ----------- | -----------|----------- |
| id | string   | profiles id |
| price  |  float   | price for one month of the profiles |
| level | integer   |profiles level 0Base 1Pro |
| envNum | integer   |profiles max environment number |
| freeTime | integer   |profiles free use minute |
| openEnvNumOneDay | integer   | environment open max number in one day |
| createEnvNumOneDay | integer   | create new environment  max number in one day |


Response Example
----------------

```json
{
    "traceId": "BBBA5FE8B3A8FBDEB0209321B43BEB80",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": "497540679501610040",
            "price": 5,
            "level": 0,
            "envNum": 5,
            "freeTime": 60,
            "openEnvNumOneDay": 1000,
            "createEnvNumOneDay": 25
        },
        {
            "id": "512719311391949750",
            "price": 19,
            "level": 1,
            "envNum": 20,
            "freeTime": 60,
            "openEnvNumOneDay": 10000,
            "createEnvNumOneDay": 200
        }
    ]
}
```

---

### Change plan

API Description
---------------

For changing plan, the API only supports upgrading plan. Downgrading plan should be completed through the GeeLark client

Request URL
-----------
- `https://openapi.geelark.com/open/v1/pay/plan/upgrade`

Request Method
--------------
- POST

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| ----------- | -------| -----------|----------- |--------- |
| profilesId   | yes     |   string  | profiles id，it can be obtained through the 'get plan list' API | 497540679501610040 |
|parallelsNum|yes|integer|the parallels number should be greater than or equal to the parallels number of the current plan| 1 |
|monthlyRentalNum|yes|integer|the monthly rental number should be greater than or equal to the monthly rental number of the current plan| 1  |
|days|no|integer| Parameter was required when the plan was expired, renewal duration：30/90/180/360 day| 30 |
|promoCode|no|string|promo code| PromoCode |

Request Example
---------------

```json
{
    "profilesId": "497540679501610040",
    "parallelsNum":1,
    "monthlyRentalNum" : 1
}
```

Response Example
----------------

```json
{
    "traceId": "A3889654BA84B91CBABF8535B83AEABB",
    "code": 0,
    "msg": "success"
}
```

Error Codes
-----------

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

| Error Code | Description |
| --- | --- |
| 41001 | balance not enough |
| 41002 | only support upgrade plan, please operate on the client side |
| 41003 | promo code is invalid |

---

### Renew plan

API Description
---------------

renew plan

Request URL
-----------
- `https://openapi.geelark.com/open/v1/pay/plan/continue`

Request Method
--------------
- POST

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| ----------- | -------| -----------|----------- |--------- |
|days|yes|integer|renewal duration：30/90/180/360 day| 30 |
|promoCode|no|string|promo code| PromoCode |

Request Example
---------------

```json
{
    "days":30,
    "promoCode" : "GeeLark666"
}
```

Response Example
----------------

```json
{
    "traceId": "A3889654BA84B91CBABF8535B83AEABB",
    "code": 0,
    "msg": "success"
}
```

Error Codes
-----------

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

| Error Code | Description |
| --- | --- |
| 41001 | balance not enough |
| 41003 | promo code is invalid |

---

### Get the current subscription plan information

[TOC]

API Description
---------------

Get the current subscription plan information.  
Rate limit: **1 request per minute**

Request URL
-----------

*   `https://openapi.geelark.com/open/v1/pay/plan/info`
    

Request Method
--------------

*   `POST`
    

Response Parameters
-------------------

| Parameter Name | Type | Description |
| --- | --- | --- |
| plan | integer | Subscription type: 0 = Base, 1 = Pro |
| profiles | integer | Total number of profiles |
| monthlyRental | integer | Number of monthly rental devices |
| parallels | integer | No extra charge as long as the number of cloud phone profiles opened at the same time does not exceed your parallel limit. |
| expirationTime | integer | Plan expiration timestamp |
| monthlyFee | float | Monthly billing amount |
| availableProfiles | integer | Number of available profiles |
|availableMonthlyRentals|integer| Number of available monthly rental devices  |

Response Example
----------------

```json
{
    "traceId": "928AD6F698AE1840ACEA9A5EA858179B",
    "code": 0,
    "msg": "success",
    "data": {
        "plan": 1,
        "profiles": 1000,
        "monthlyRental": 13,
        "parallels": 3,
        "expirationTime": 1774596449,
        "monthlyFee": 777.4,
        "availableProfiles": 160,
        "availableMonthlyRentals": 0
    }
}
```

---

### Billing transaction detail

[toc]

API Description
---------------

Query billing transaction detail

Request URL
-----------
- `https://openapi.geelark.com/open/v1/billing/transaction/detail`

Request Method
--------------
- POST

Request Parameters
------------------

| Parameter | Required | Type | Description | Example |
| ----------- | -------| -----------|----------- |--------- |
| id | No | string | Specify the cloud phone ID. If not specified, will be obtained all | "612451567282427943" |
| startAt | No | integer | Filter start time, second-level timestamp (currently only supports searching data within the last 3 days) | 1774593838 |
| endAt | No | integer| Filtering end time, second-level timestamp (currently only supports searching data within the last 3 days)|1774593838|
| limit | No | integer | The acquisition quantity limit is set to 100 by default, with a maximum of 1000 |1 |
| lastFlowId | No | string | The lastFlowId returned from the previous request is used to obtain the data for the next page | "612476158453291064" |

Request Example
---------------

```json
{
	"id": "612451567282427943",
	"limit" : 10,
	"lastFlowId": "612476158453291064",
	"startAt" : 1774593838,
	"endAt": 1774593840
}
```

Response Example
----------------

```json
{
	"traceId": "9DBBF7A080B099189E2D84CF92287189",
	"code": 0,
	"msg": "success",
	 "data": {
		"total": 1,
		"page": 1,
		"pageSize": 10,
		"list": [
			{
				"id": "612451567282427943",
				"envId": "612451567282427942",
				"amount": 0,
				"usedTime": 2,
				"type": 1,
				"chargeType": 5,
				"createdTime": 1774593838
			}
		],
		"lastFlowId" : "612451567282427943"
	}
}
```

Response Body Description
-------------------------

| Parameter | Type | Description |
| ----------- | -----------|----------- |
| id | string | flow id |
| envId | string | cloud phone id |
| type | integer | Usage type ，1-cloud phone  2-RPA |
| chargeType | integer | Billing type 1-Points 2-Balance 3-Bonus 4-Time add-on 5-Bonus minutes 6-Monthly rental 7-Parallels  8-Daily cap reached|
| amount | float | amount |
| usedTime | integer | Usage duration, minutes|
| createdTime | integer | flow created time, second-level timestamp |
| lastFlowId | string | The last sequential ID, used to retrieve data from the next page |


Response Example
----------------

Error Codes
-----------

Please refer to the [Cloud Phone Error Codes](https://open.geelark.com/api/cloud-phone-error-codes)

---

## Error Codes

### Cloud Phone Error Codes

Global
------
```
0 Success
40000 Unknown error
40001 Failed to read request body
40002 traceId is empty
40003 Signature verification failed
40004 Parameter validation failed
40005 Resource not found
40006 Partial success for batch operation
40009 Batch operation failed completely
40007 Request rate limited
40008 pageSize exceeds maximum/minimum limit
40010 Resource is occupied and cannot be deleted
40011 Available to paid users only
40012 API is deprecated, please use the latest version
40013 User not found
40014 API request exceeds hourly limit; locked for two hours
40015 Insufficient permissions
40016 The IP address is not within the whitelist
40017 Too many requests, please try again later
50000 Internal server error
```

* * *

Cloud Phone
-----------
```
42001 Cloud phone not found
43002 User is not on a Pro plan and cannot perform this operation
43004 Cloud phone has expired
43005 Cloud phone is executing a task; delete/refresh operations are not allowed
43006 Cloud phone is under remote control; delete/refresh operations are not allowed
43009 Cloud phone has already been opened; delete/refresh operations are not allowed
43010 Cloud phone is starting; delete/refresh operations are not allowed
43021 Cloud phone is in use; delete/refresh operations are not allowed
43008 Daily cloud phone open limit reached (UTC timezone)
43011 Cloud phone is performing a one-click new machine and cannot be operated
43012 Cloud phone GPS information error
43013 Cloud phone plugin installation task does not exist
43014 GPS is not set
43015 Cloud phone does not support one-click refresh
43016 Cloud phone does not support root temporarily
43017 No monthly subscription device available
43018 Cloud phone is not bound to a monthly subscription device
43019 Only monthly subscription type is supported
43020 Cloud phone backup data exception
43022 Cannot transfer profile to yourself
43023 Profile name is empty
43024 Brand and model do not match
43025 Language not supported
43026 System not supported
43027 Browser does not support transfer
43028 Sub-user profile group limitation
43029 Selected cloud phone model is under maintenance, please try again later
43036 Cloud phone is running and cannot perform this operation
43037 Accessibility hiding is not supported
43038 The device model has been deleted
43039 Currently unavailable; maintenance in progress
49001 ADB is not enabled
49002 Device model does not support ADB
50001 Device model does not support shell
52001 Device model does not support sending SMS
53001 Device model does not support installing patches
```

* * *

App
---
```
42002 Cloud phone is not in running state
42003 The specified app is being installed
42004 Installing a lower app version is not allowed
42005 The specified app is not installed
42006 The specified app does not exist
42007 Upload task not found
```

* * *

Tags
----
```
43020 Tag name is empty
43021 Tag already exists
43022 Tag does not exist
43023 Tag color does not exist
43024 Tag name does not exist

```

* * *

Groups
------
```
43030 Group name is empty
43031 Group already exists
43032 Group does not exist
43033 Group name does not exist
43034 Group remark does not exist
43035 Ungrouped items cannot be edited
```

* * *

Create Cloud Phone
------------------
```
44001 Pro plan limitation
44002 Profiles count has reached the plan limit
44003 User profiles count has reached the limit
44004 Daily profiles creation limit reached
44005 Group is not specified
44006 Cloud phone inventory is insufficient
```

* * *

Proxy
-----
```
43001 Related profiles exist; deletion is not allowed
45001 Proxy does not exist
45002 Proxy is unavailable
45003 Proxy is not supported (proxy server IP or Outbound IP is located in mainland China)
45004 Proxy validation failed
45005 Region not supported
45006 Invalid proxy information
45007 Duplicate proxy
45008 Proxy type not supported

```

* * *

Plan
----
```
46001 Plan has expired
46002 Team profiles count exceeds plan limit
46003 Owned profiles count exceeds plan limit

```

* * *

Device
------
```
47001 Device concurrency limit reached
47002 All devices are in use
47003 Related device has expired
47004 Related device does not exist

```

* * *

Task
----
```
42008 Invalid app version; only specified app versions are allowed for task creation
48000 Task retry limit exceeded; further retries are not allowed
48001 Task status is already success or failure; further operations are not allowed
48002 Task does not exist
48003 Task material has expired
48004 TikTok task requires a specific app version; only specified versions are allowed
41000 Insufficient task points
41001 Insufficient balance

```

* * *

Material Center
---------------
```
60001 Material library capacity exceeded
60002 Duplicate tag name
60003 Invalid URL
60004 File format not supported
60005 Material does not exist

```

* * *

Others
------

```
51001 User callback does not exist
```

---

### Browser Error Codes

Global Error Codes
------------------

| Code | Message |
| --- | --- |
| 0 | Success |
| 40000 | Unknown error |
| 40001 | Failed to read request body |
| 40002 | `traceId` is missing |
| 40003 | Signature verification failed |
| 40004 | Invalid request parameters |
| 40005 | Resource not found |
| 40006 | Batch operation partially succeeded |
| 40007 | Request rate limit exceeded |
| 40008 | `pageSize` is out of allowed range |
| 40009 | Batch operation failed |
| 40010 | Resource is currently in use and cannot be deleted |
| 40011 | This API is available to paid users only |
| 40012 | This API has been deprecated. Please use the latest version |
| 40013 | User does not exist |
| 40014 | Hourly API request limit exceeded. Access is locked for 2 hours |
| 40015 | Permission denied |
| 50000 | Internal server error |
| 90000 | Invalid argument. |
| 90001 | User not logged in. |
| 90002 | id not found. |
| 90003 | Insufficient disk space. |
| 90004 | API permission denied. |
| 90005 | Not supported on Linux. |
| 90006 | Permission denied to start or close. |
| 90007 | Missing 'Authorization' in the header. |

* * *

Environment Error Codes
-----------------------

| Code | Message |
| --- | --- |
| 43022 | Cannot transfer the environment to yourself |
| 43023 | Environment name is required |
| 43028 | Sub-user environment group limit exceeded |

* * *

Tag Error Codes
---------------

| Code | Message |
| --- | --- |
| 43020 | Tag name is required |
| 43021 | Tag already exists |
| 43022 | Tag does not exist |
| 43023 | Tag color does not exist |
| 43024 | Tag name does not exist |

* * *

Group Error Codes
-----------------

| Code | Message |
| --- | --- |
| 43030 | Group name is required |
| 43031 | Group already exists |
| 43032 | Group does not exist |
| 43033 | Group name does not exist |
| 43034 | Group remark does not exist |
| 43035 | Ungrouped items cannot be edited |

* * *

Create Environment Error Codes
------------------------------

| Code | Message |
| --- | --- |
| 44001 | Restricted by Pro plan |
| 44002 | Environment count has reached the plan limit |
| 44003 | User environment count limit exceeded |
| 44004 | Daily environment creation limit exceeded |
| 44005 | Group is required |

* * *

Proxy Error Codes
-----------------

| Code | Message |
| --- | --- |
| 43001 | Cannot delete proxy with associated environments |
| 45001 | Proxy not found |
| 45002 | Proxy is unavailable |
| 45003 | Proxy is not supported (proxy server IP or exit IP is located in Mainland China) |
| 45004 | Proxy validation failed |
| 45005 | Region not supported |
| 45006 | Invalid proxy configuration |
| 45007 | Duplicate proxy |
| 45008 | Proxy type not supported |

* * *

Plan Error Codes
----------------

| Code | Message |
| --- | --- |
| 46001 | Plan has expired |
| 46002 | Team environment count exceeds plan limit |
| 46003 | Environment count exceeds plan limit |

* * *

Asset Center Error Codes
------------------------

| Code | Message |
| --- | --- |
| 60001 | Asset storage capacity exceeded |
| 60002 | Duplicate tag name |
| 60003 | Invalid URL |
| 60004 | File format not supported |
| 60005 | Asset not found |

* * *

---

## API Document Download

### API Document Download

### Markdown Document Download, can be fed to AI to help auto-generate code: [Download](https://material.geelark.com/openapi-doc/en-doc.zip)

---
