/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */


import ApiClient from "../ApiClient";
import HTTPValidationError from '../model/HTTPValidationError';
import Message from '../model/Message';

/**
* Messages service.
* @module api/MessagesApi
* @version 0.1.0
*/
export default class MessagesApi {

    /**
    * Constructs a new MessagesApi. 
    * @alias module:api/MessagesApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }


    /**
     * Callback function to receive the result of the getMessagesSessionsMessagesGet operation.
     * @callback module:api/MessagesApi~getMessagesSessionsMessagesGetCallback
     * @param {String} error Error message, if any.
     * @param {Array.<module:model/Message>} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get Messages
     * @param {String} sessionId 
     * @param {module:api/MessagesApi~getMessagesSessionsMessagesGetCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link Array.<module:model/Message>}
     */
    getMessagesSessionsMessagesGet(sessionId, callback) {
      let postBody = null;
      // verify the required parameter 'sessionId' is set
      if (sessionId === undefined || sessionId === null) {
        throw new Error("Missing the required parameter 'sessionId' when calling getMessagesSessionsMessagesGet");
      }

      let pathParams = {
      };
      let queryParams = {
        'session_id': sessionId
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = [Message];
      return this.apiClient.callApi(
        '/sessions/messages/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }


}
