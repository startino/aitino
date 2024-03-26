# FastApi.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**autoBuildCrewAutoBuildGet**](DefaultApi.md#autoBuildCrewAutoBuildGet) | **GET** /auto-build | Auto Build Crew
[**compileCompileGet**](DefaultApi.md#compileCompileGet) | **GET** /compile | Compile
[**improveImproveGet**](DefaultApi.md#improveImproveGet) | **GET** /improve | Improve
[**redirectToDocsGet**](DefaultApi.md#redirectToDocsGet) | **GET** / | Redirect To Docs



## autoBuildCrewAutoBuildGet

> String autoBuildCrewAutoBuildGet(generalTask, profileId)

Auto Build Crew

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.DefaultApi();
let generalTask = "generalTask_example"; // String | 
let profileId = "profileId_example"; // String | 
apiInstance.autoBuildCrewAutoBuildGet(generalTask, profileId, (error, data, response) => {
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
 **generalTask** | **String**|  | 
 **profileId** | **String**|  | 

### Return type

**String**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## compileCompileGet

> {String: ResponseCompileCompileGet} compileCompileGet(id)

Compile

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.DefaultApi();
let id = "id_example"; // String | 
apiInstance.compileCompileGet(id, (error, data, response) => {
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
 **id** | **String**|  | 

### Return type

[**{String: ResponseCompileCompileGet}**](ResponseCompileCompileGet.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## improveImproveGet

> String improveImproveGet(wordLimit, prompt, promptType, temperature, profileId)

Improve

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.DefaultApi();
let wordLimit = 56; // Number | 
let prompt = "prompt_example"; // String | 
let promptType = "promptType_example"; // String | 
let temperature = 3.4; // Number | 
let profileId = "profileId_example"; // String | 
apiInstance.improveImproveGet(wordLimit, prompt, promptType, temperature, profileId, (error, data, response) => {
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
 **wordLimit** | **Number**|  | 
 **prompt** | **String**|  | 
 **promptType** | **String**|  | 
 **temperature** | **Number**|  | 
 **profileId** | **String**|  | 

### Return type

**String**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## redirectToDocsGet

> Object redirectToDocsGet()

Redirect To Docs

### Example

```javascript
import FastApi from 'fast_api';

let apiInstance = new FastApi.DefaultApi();
apiInstance.redirectToDocsGet((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

