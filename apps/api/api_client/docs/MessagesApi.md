# FastApi.MessagesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getMessagesSessionsMessagesGet**](MessagesApi.md#getMessagesSessionsMessagesGet) | **GET** /sessions/messages/ | Get Messages



## getMessagesSessionsMessagesGet

> [Message] getMessagesSessionsMessagesGet(sessionId)

Get Messages

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.MessagesApi();
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

