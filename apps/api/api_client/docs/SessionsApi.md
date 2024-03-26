# FastApi.SessionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deleteSessionSessionsDeletePost**](SessionsApi.md#deleteSessionSessionsDeletePost) | **POST** /sessions/delete | Delete Session
[**getMessagesSessionsMessagesGet**](SessionsApi.md#getMessagesSessionsMessagesGet) | **GET** /sessions/messages/ | Get Messages
[**getSessionsSessionsPost**](SessionsApi.md#getSessionsSessionsPost) | **POST** /sessions/ | Get Sessions
[**insertSessionSessionsInsertPost**](SessionsApi.md#insertSessionSessionsInsertPost) | **POST** /sessions/insert | Insert Session
[**runCrewSessionsRunPost**](SessionsApi.md#runCrewSessionsRunPost) | **POST** /sessions/run | Run Crew
[**updateSessionSessionsUpdatePost**](SessionsApi.md#updateSessionSessionsUpdatePost) | **POST** /sessions/update | Update Session
[**upsertSessionSessionsUpsertPost**](SessionsApi.md#upsertSessionSessionsUpsertPost) | **POST** /sessions/upsert | Upsert Session



## deleteSessionSessionsDeletePost

> Boolean deleteSessionSessionsDeletePost(sessionId)

Delete Session

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let sessionId = "sessionId_example"; // String | 
apiInstance.deleteSessionSessionsDeletePost(sessionId, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sessionId** | **String**|  | 

### Return type

**Boolean**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getMessagesSessionsMessagesGet

> [Message] getMessagesSessionsMessagesGet(sessionId)

Get Messages

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let sessionId = "sessionId_example"; // String | 
apiInstance.getMessagesSessionsMessagesGet(sessionId, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sessionId** | **String**|  | 

### Return type

[**[Message]**](Message.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getSessionsSessionsPost

> [Session] getSessionsSessionsPost(opts)

Get Sessions

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let opts = {
  'profileId': "profileId_example", // String | 
  'sessionId': "sessionId_example" // String | 
};
apiInstance.getSessionsSessionsPost(opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profileId** | **String**|  | [optional] 
 **sessionId** | **String**|  | [optional] 

### Return type

[**[Session]**](Session.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## insertSessionSessionsInsertPost

> Boolean insertSessionSessionsInsertPost(sessionId, body)

Insert Session

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let sessionId = "sessionId_example"; // String | 
let body = {key: null}; // Object | 
apiInstance.insertSessionSessionsInsertPost(sessionId, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sessionId** | **String**|  | 
 **body** | **Object**|  | 

### Return type

**Boolean**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## runCrewSessionsRunPost

> Object runCrewSessionsRunPost(runRequestModel, opts)

Run Crew

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let runRequestModel = new FastApi.RunRequestModel(); // RunRequestModel | 
let opts = {
  'mock': false // Boolean | 
};
apiInstance.runCrewSessionsRunPost(runRequestModel, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **runRequestModel** | [**RunRequestModel**](RunRequestModel.md)|  | 
 **mock** | **Boolean**|  | [optional] [default to false]

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateSessionSessionsUpdatePost

> Boolean updateSessionSessionsUpdatePost(sessionId, body)

Update Session

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let sessionId = "sessionId_example"; // String | 
let body = {key: null}; // Object | 
apiInstance.updateSessionSessionsUpdatePost(sessionId, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sessionId** | **String**|  | 
 **body** | **Object**|  | 

### Return type

**Boolean**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## upsertSessionSessionsUpsertPost

> Boolean upsertSessionSessionsUpsertPost(sessionId, body)

Upsert Session

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.SessionsApi();
let sessionId = "sessionId_example"; // String | 
let body = {key: null}; // Object | 
apiInstance.upsertSessionSessionsUpsertPost(sessionId, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sessionId** | **String**|  | 
 **body** | **Object**|  | 

### Return type

**Boolean**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

