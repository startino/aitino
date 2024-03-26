# FastApi.CrewsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**insertCrewCrewsPost**](CrewsApi.md#insertCrewCrewsPost) | **POST** /crews/ | Insert Crew



## insertCrewCrewsPost

> Object insertCrewCrewsPost(crewRequestModel)

Insert Crew

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.CrewsApi();
let crewRequestModel = new FastApi.CrewRequestModel(); // CrewRequestModel | 
apiInstance.insertCrewCrewsPost(crewRequestModel, (error, data, response) => {
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
 **crewRequestModel** | [**CrewRequestModel**](CrewRequestModel.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

