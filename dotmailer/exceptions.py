# -*- coding: utf8 -*-


class ErrorAccountInvalid(Exception):
    """
    DotMailer Exception: ERROR_ACCOUNT_INVALID
    """
    message = 'The account is not valid. This means you are trying to ' \
              'reference an account that doesn\'t exist or has certain' \
              ' restrictions placed upon it. Please contact DotMailer\'s' \
              ' support department if you require assistance.'


class ErrorAddressbookDuplicate(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_DUPLICATE
    """
    message = 'There is already an address book with that name in the ' \
              'account. Please make sure that the name of the address book ' \
              'you are using is unique and not one of the reserved address ' \
              'book names such as \'Test\' or \'All Contacts\'.'


class ErrorAddressbookInUse(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_IN_USE
    """
    message = 'The address book you are attempting to use in your request is' \
              ' in use - retrying later may succeed.'


class ErrorAddressbookInvalid(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_INVALID
    """
    message = 'This address book is not valid. This means that there is ' \
              'something incorrect with the address book object you are ' \
              'sending to the method/operation, or you are referring to ' \
              'a non-existent address book. Check that your address book ' \
              'object is valid by checking the definition in the ' \
              'documentation.'


class ErrorAddressbookLimitExceeded(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_LIMITEXCEEDED
    """
    message = 'Your account will have a limited number of address books, ' \
              'which depends on the level of account you\'re using. You ' \
              'have currently exceeded this limit. Please delete some of ' \
              'your unused address books.'


class ErrorAddressbookNotFound(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_NOT_FOUND
    """
    message = 'The address book you have specified with the addressBookId ' \
              'argument does not relate to an address book which exists in' \
              ' the account you are currently connected to.'


class ErrorAddressbookNotwritable(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_NOTWRITABLE
    """
    message = 'The address book you have specified with the addressBookId ' \
              'argument relates to an address book which cannot be written ' \
              'to. For example, you cannot upload contacts to the \'Test\' ' \
              'address book via the API.'


class ErrorAddressbookToomany(Exception):
    """
    DotMailer Exception: ERROR_ADDRESSBOOK_TOOMANY
    """
    message = 'You have reached the maximum number of address books ' \
              'permitted for your account type'


class ErrorApiusageExceeded(Exception):
    """
    DotMailer Exception: ERROR_APIUSAGE_EXCEEDED
    """
    message = 'The last method/operation call you made exceeded the cut-off ' \
              'of 2000  API calls in a one hour period. You will be unable ' \
              'to make any further API calls until the number of API calls ' \
              'made in the last hour goes below this figure. Please review ' \
              'your code to determine what is causing this excess usage.'


class ErrorApiuserInvalid(Exception):
    """
    DotMailer Exception: ERROR_APIUSER_INVALID
    """
    message = 'The API user credentials that you have used in the request ' \
              'are invalid. You may have entered them incorrectly. Please ' \
              'check that your credentials are being entered correctly.'


class ErrorBodyDoesNotMatchContentType(Exception):
    """
    DotMailer Exception: ERROR_BODY_DOES_NOT_MATCH_CONTENT_TYPE
    """
    message = 'The body of your request does not match the content type. ' \
              'Please check that the content type is set correctly.'


class ErrorCampaignInvalid(Exception):
    """
    DotMailer Exception: ERROR_CAMPAIGN_INVALID
    """
    message = 'The campaign that you are attempting to create has some ' \
              'invalid properties. Please check the settings you are using ' \
              'for this campaign.'


class ErrorCampaignNotFound(Exception):
    """
    DotMailer Exception: ERROR_CAMPAIGN_NOT_FOUND
    """
    message = 'The campaign you are trying to get could not be found within ' \
              'the account. It is likely that you are using the incorrect ' \
              'ID number.'


class ErrorCampaignReadonly(Exception):
    """
    DotMailer Exception: ERROR_CAMPAIGN_READONLY
    """
    message = 'The campaign you are trying to update cannot be updated - ' \
              'please check that you have the right ID.'


class ErrorCampaignSendInvalid(Exception):
    """
    DotMailer Exception: ERROR_CAMPAIGN_SEND_INVALID
    """
    message = 'The campaign send is not valid. This means that there is ' \
              'something incorrect with the campaign send object you are ' \
              'sending to the method/operation. Check that your campaign ' \
              'send object is valid by checking the definition in the ' \
              'documentation.'


class ErrorCampaignSendnotpermitted(Exception):
    """
    DotMailer Exception: ERROR_CAMPAIGN_SENDNOTPERMITTED
    """
    message = 'We cannot permit you to send this campaign. This will most ' \
              'likely be because your account is not fully enabled.'


class ErrorCannotPerformOpersationOnAccount(Exception):
    """
    DotMailer Exception: ERROR_CANNOT_PERFORM_OPERATION_ON_ACCOUNT
    """
    message = 'The operation that your request is trying to perform can’t ' \
              'be executed on your account.'


class ErrorContactAreNotSpecified(Exception):
    """
    DotMailer Exception: ERROR_CONTACTS_ARE_NOT_SPECIFIED
    """
    message = 'The request you are making is not specifying the contacts ' \
              'that are required. Make sure you have included these in your ' \
              'request.'


class ErrorContactInvalid(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_INVALID
    """
    message = 'The contact you are trying to add is not valid. This means ' \
              'that there is something incorrect with the contact object ' \
              'you are sending to the method/operation. Check that your ' \
              'contact object is valid by checking the definition in the ' \
              'documentation.'


class ErrorContactNotFound(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_NOT_FOUND
    """
    message = 'The ID of the contact you have selected is not present ' \
              'within the account.'


class ErrorContactRebsubscriptionInvalid(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_RESUBSCRIPTION_INVALID
    """
    message = 'The contact resubscription is not valid. This means that ' \
              'there is something incorrect with the contact resubscription ' \
              'object you are sending to the method/operation. Check that ' \
              'your contact resubscription object is valid by checking the ' \
              'definition in the documentation.'


class ErrorContactSuppressed(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_SUPPRESSED
    """
    message = 'The contact you are trying to add to the address book has ' \
              'been suppressed. This means that you cannot add the contact ' \
              'back into the address book or the account.'


class ErrorContactSuppressedforaddressbook(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_SUPPRESSEDFORADDRESSBOOK
    """
    message = 'The contact you are attempting to add is suppressed for this ' \
              'address book.'


class ErrorContactToomany(Exception):
    """
    DotMailer Exception: ERROR_CONTACT_TOOMANY
    """
    message = 'You have exceeded the number of contacts permitted for your ' \
              'account type. Please consider upgrading your account.'


class ErrorContentTypeIsNotSupported(Exception):
    """
    DotMailer Exception: ERROR_CONTENT_TYPE_IS_NOT_SUPPORTED
    """
    message = 'The content type is not supported. Please check that you have' \
              ' set a supported content type for your request.'


class ErrorDatafieldInvalid(Exception):
    """
    DotMailer Exception: ERROR_DATAFIELD_INVALID
    """
    message = 'The data field is not valid. This means that there is ' \
              'something incorrect with the data field object you are ' \
              'sending to the method/operation, or you are referring to a ' \
              'non-existent data field. Check that your data field object ' \
              'is valid by checking the definition in the documentation.'


class ErrorDatafieldLimitexceeded(Exception):
    """
    DotMailer Exception: ERROR_DATAFIELD_LIMITEXCEEDED
    """
    message = 'You currently have more than the allowed contact data ' \
              'fields in your account, despite the fact that we advertise ' \
              'unlimited contact data fields per account for some account ' \
              'levels. Please delete some of your unused contact data ' \
              'fields in order to create more.'


class ErrorDatafieldNotfound(Exception):
    """
    DotMailer Exception: ERROR_DATAFIELD_NOTFOUND
    """
    message = 'One or more of the contact data fields you are trying to set ' \
              'for the contact does not exist. Please make sure that you ' \
              'create any required  contact data fields before attempting ' \
              'to assign values to them.'


class ErrorDatafieldValueOverflow(Exception):
    """
    DotMailer Exception: ERROR_DATAFIELD_VALUE_OVERFLOW
    """
    message = 'There has been a data field value overflow.'


class ErrorDocumentAttachmentstoolarge(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_ATTACHMENTSTOOLARGE
    """
    message = 'Your attachments are too large. They have reached the ' \
              'maximum limit. Please reduce the size.'


class ErrorDocumentDataempty(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_DATAEMPTY
    """
    message = 'There is no data supplied for this document object. Please ' \
              'ensure this document exists in your account and has valid data.'


class ErrorDocumentFolderInvalid(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_FOLDER_INVALID
    """
    message = 'The document folder is not valid. This means that there is ' \
              'something incorrect with the document folder object you are ' \
              'sending to the method/operation. Check that your document ' \
              'folder object is valid by checking the definition in the ' \
              'documentation.'


class ErrorDocumentFolderNotFound(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_FOLDER_NOT_FOUND
    """
    message = 'The document folder could not be found within the account. ' \
              'Either it has been deleted or it is likely that you are ' \
              'using the incorrect ID number.'


class ErrorDocumentInvalid(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_INVALID
    """
    message = 'The document is not valid. This means that there is ' \
              'something incorrect with the document object you are sending ' \
              'to the method/operation. Check that your document object is ' \
              'valid by checking the definition in the documentation.'


class ErrorDocumentNameinvalid(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_NAMEINVALID
    """
    message = 'The document provided has an invalid name. Please check that ' \
              'the name is correct.'


class ErrorDocumentNotFound(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_NOT_FOUND
    """
    message = 'The document object could not be found within the account. ' \
              'Either it has been deleted or it is likely that you are ' \
              'using the incorrect ID number.'


class ErrorDocumentToolarge(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_TOOLARGE
    """
    message = 'The document that you\'re attempting to add is too large. ' \
              'It exceeds the maximum size of 10MB.'


class ErrorDocumentToomanyattachments(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_TOOMANYATTACHMENTS
    """
    message = 'Your campaign has reached the maximum amount of attachments ' \
              'it is allowed to have. Please reduce this amount.'


class ErrorDocumentUnsupportedformat(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_UNSUPPORTEDFORMAT
    """
    message = 'The document is not in a supported format. Please ensure you ' \
              'use the correct format.'


class ErrorDocumentAlreadyattached(Exception):
    """
    DotMailer Exception: ERROR_DOCUMENT_ALREADYATTACHED
    """
    message = 'You are attempting to attach a document object that is ' \
              'already attached to this campaign.'


class ErrorEnrolmentAllowanceExceeded(Exception):
    """
    DotMailer Exception: ERROR_ENROLMENT_ALLOWANCE_EXCEEDED
    """
    message = 'You have exceeded the limit of 20 calls per hour for ' \
              'creating program enrolments across all programs. You will be ' \
              'unable to make any further calls to create program ' \
              'enrolments until the number made in the last hour goes below ' \
              'this figure.'


class ErrorEnrolmentInvalid(Exception):
    """
    DotMailer Exception: ERROR_ENROLMENT_INVALID
    """
    message = 'The program enrolment you are trying to create or retrieve ' \
              'is not valid. This means that there is something incorrect ' \
              'with the enrolment object you are sending to the ' \
              'method/operation. Check that your enrolment object is valid ' \
              'by checking the definition in the documentation.'


class ErrorEnrolmentIsProcessing(Exception):
    """
    DotMailer Exception: ERROR_ENROLMENT_IS_PROCESSING
    """
    message = 'The program enrolment faults report in your request can\'t ' \
              'be retrieved because the enrolment is still processing.'


class ErrorEnrolmentNotFound(Exception):
    """
    DotMailer Exception: ERROR_ENROLMENT_NOT_FOUND
    """
    message = 'The program enrolment you are trying to retrieve or ' \
              'reference in your call does not exist. Please make sure that ' \
              'the program enrolment ID (GUID) you are using is correct.'


class ErrorFeaturenoactive(Exception):
    """
    DotMailer Exception: ERROR_FEATURENOTACTIVE
    """
    message = 'The feature your call is referencing is not active on your ' \
              'account (e.g. transactional email). Please make sure this ' \
              'feature is enabled before calling it again.'


class ErrorImageDataempty(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_DATAEMPTY
    """
    message = 'There is no data supplied for this image object. Please ' \
              'ensure this image exists in your account and has valid data.'


class ErrorImageFolderNotFound(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_FOLDER_NOT_FOUND
    """
    message = 'The ID of the image folder could not be found within the ' \
              'account. Either it has been deleted or it is likely that ' \
              'you are using the incorrect ID number.'


class ErrorImageFolderDeleted(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_FOLDER_DELETED
    """
    message = 'The image folder you have selected has been deleted.'


class ErrorImageFolderInvalid(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_FOLDER_INVALID
    """
    message = 'The image folder is not valid. This means that there is ' \
              'something incorrect with the image folder object you are ' \
              'sending to the method/operation. Check that your image ' \
              'folder object is valid by checking the definition in the ' \
              'documentation.'


class ErrorImageInvalid(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_INVALID
    """
    message = 'The image is not valid. This means that there is something ' \
              'incorrect with the image object you are sending to the ' \
              'method/operation. Check that your image object is valid by ' \
              'checking the definition in the documentation.'


class ErrorImageNameinvalid(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_NAMEINVALID
    """
    message = 'The image object provided has an invalid name. Please check ' \
              'that the name is correct.'


class ErrorImageParentfolderisfull(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_PARENTFOLDERISFULL
    """
    message = 'The parent image folder that you are attempting to add the ' \
              'child folder to is now full.'


class ErrorImageUnsupportedformat(Exception):
    """
    DotMailer Exception: ERROR_IMAGE_UNSUPPORTEDFORMAT
    """
    message = 'The image object is not in a supported format. Please ' \
              'ensure you use the correct format.'


class ErrorImportNotFound(Exception):
    """
    DotMailer Exception: ERROR_IMPORT_NOT_FOUND
    """
    message = 'The GUID you have provided does not relate to an import in ' \
              'our system. Please check that you are entering the correct ' \
              'GUID.'


class ErrorImportReportNotFound(Exception):
    """
    DotMailer Exception: ERROR_IMPORT_REPORT_NOT_FOUND
    """
    message = 'The import report object could not be found within the ' \
              'account. Please check that you are entering the correct GUID.'


class ErrorImportToomanyactiveimports(Exception):
    """
    DotMailer Exception: ERROR_IMPORT_TOOMANYACTIVEIMPORTS
    """
    message = 'You currently have more than four imports running in one go.'


class ErrorImportUnsupportedFormat(Exception):
    """
    DotMailer Exception: ERROR_IMPORT_UNSUPPORTED_FORMAT
    """
    message = 'The import object is not in a supported format. Please ' \
              'ensure you use the correct format.'


class ErrorInvalidApiuserexists(Exception):
    """
    DotMailer Exception: ERROR_INVALID_APIUSEREXISTS
    """
    message = 'You cannot attempt to recreate an API user which already ' \
              'exists.'


class ErrorInvalidEmail(Exception):
    """
    DotMailer Exception: ERROR_INVALID_EMAIL
    """
    message = 'The email address of the contact you are adding is invalid. ' \
              'Each contact object must contain a valid email address.'


class ErrorInvalidLogin(Exception):
    """
    DotMailer Exception: ERROR_INVALID_LOGIN
    """
    message = 'The username or password you are attempting to authenticate ' \
              'your method call with is invalid. Please make sure you have ' \
              'used the correct details. If your login attempt is still ' \
              'unsuccessful please follow the steps to reset your username ' \
              'and password as set out in the documentation. This error is ' \
              'also returned if the account you are attempting to connect ' \
              'to is turned off or disabled.'


class ErrorMalformedRequest(Exception):
    """
    DotMailer Exception: ERROR_MALFORMED_REQUEST
    """
    message = 'Your request is not formed correctly. Please check our ' \
              'documentation to make sure you have included all of the ' \
              'required parameters in your request and that it is formed ' \
              'correctly.'


class ErrorManagedUserInvalid(Exception):
    """
    DotMailer Exception: ERROR_MANAGED_USER_INVALID
    """
    message = 'The API managed user credentials that you have used in the ' \
              'request are invalid. You may have entered them incorrectly. ' \
              'Please check that the managed user credentials are being ' \
              'entered correctly.'


class ErrorMissingSetupkeyvalues(Exception):
    """
    DotMailer Exception: ERROR_MISSING_SETUPKEYVALUES
    """
    message = 'You have not included all setup keys.'


class ErrorMultiFileUploadNotAllowed(Exception):
    """
    DotMailer Exception: ERROR_MULTI_FILE_UPLOAD_NOT_ALLOWED
    """
    message = 'You have attempted to upload multiple files in a call, which ' \
              'isn\'t allowed. Please upload one file per call.'


class ErrorNoEmailColumn(Exception):
    """
    DotMailer Exception: ERROR_NO_EMAIL_COLUMN
    """
    message = 'The data file you are attempting to import does not contain ' \
              'an Email column. This column is required when importing a ' \
              'file of data.'


class ErrorNonUniqueDatafield(Exception):
    """
    DotMailer Exception: ERROR_NON_UNIQUE_DATAFIELD
    """
    message = 'The data field you are trying to create already exists within' \
              ' the account you are connected to. Please either use the ' \
              'existing data field or choose a different name.'


class ErrorNonUniqueEmail(Exception):
    """
    DotMailer Exception: ERROR_NON_UNIQUE_EMAIL
    """
    message = 'The email address that you are trying to use is not unique.'


class ErrorOauthTokenInvalid(Exception):
    """
    DotMailer Exception: ERROR_OAUTH_TOKEN_INVALID
    """
    message = 'The OAuth token being entered with the call is invalid. You ' \
              'may have entered it incorrectly. Please check that the OAuth ' \
              'token is being entered correctly.'


class ErrorParameterInvalid(Exception):
    """
    DotMailer Exception: ERROR_PARAMETER_INVALID
    """
    message = 'One of the method/operation arguments you are sending is ' \
              'invalid.'


class ErrorProgramNotActive(Exception):
    """
    DotMailer Exception: ERROR_PROGRAM_NOT_ACTIVE
    """
    message = 'You are attempting to create a program enrolment for a ' \
              'program that isn\'t yet active. A program must be active ' \
              'before it can enrol.'


class ErrorProgramNotFound(Exception):
    """
    DotMailer Exception: ERROR_PROGRAM_NOT_FOUND
    """
    message = 'The program you are trying to retrieve or reference in your ' \
              'call does not exist. Please make sure that the program ID you' \
              ' are using is correct.'


class ErrorSegmentNotFound(Exception):
    """
    DotMailer Exception: ERROR_SEGMENT_NOT_FOUND
    """
    message = 'The segment object could not be found within the account. ' \
              'Either it has been deleted or it is likely that you are using' \
              ' the incorrect ID number.'


class ErrorSendLimitexceeded(Exception):
    """
    DotMailer Exception: ERROR_SEND_LIMITEXCEEDED
    """
    message = 'You have exceeded the amount of sends your account is allowed' \
              ' this month. Please contact your account manager if you wish ' \
              'to send more.'


class ErrorSmsInvalid(Exception):
    """
    DotMailer Exception: ERROR_SMS_INVALID
    """
    message = 'The SMS is not valid. This means that there is something ' \
              'incorrect with the SMS object you are sending to the ' \
              'method/operation. Check that your SMS object is valid by ' \
              'checking the definition in the documentation.'


class ErrorSmsInvalidphonenumber(Exception):
    """
    DotMailer Exception: ERROR_SMS_INVALIDPHONENUMBER
    """
    message = 'The phone number you have attempted to send to is invalid.'


class ErrorSmsSendnotpermitted(Exception):
    """
    DotMailer Exception: ERROR_SMS_SENDNOTPERMITTED
    """
    message = 'You do not have sufficient credit within your account for ' \
              'this SMS send. Please contact your account manager if you ' \
              'need more sending credits.'


class ErrorSurveyNotFound(Exception):
    """
    DotMailer Exception: ERROR_SURVEY_NOT_FOUND
    """
    message = 'The survey you are trying to retrieve or reference in your ' \
              'call does not exist. Please make sure that the survey ID you ' \
              'are using is correct.'


class ErrorSystemServicetemporarilyunavailable(Exception):
    """
    DotMailer Exception: ERROR_SYSTEM_SERVICETEMPORARILYUNAVAILABLE
    """
    message = 'The API is temporarily down, most likely for scheduled ' \
              'maintenance, for which you should have received notification;' \
              ' if you did not please subscribe to our user warning list to ' \
              'be notified of these updates in future.'


class ErrorTransactionalDataCollectionDoesNotExist(Exception):
    """
    DotMailer Exception: ERROR_TRANSACTIONAL_DATA_COLLECTION_DOES_NOT_EXIST
    """
    message = 'The transactional data collection you are trying to retrieve ' \
              'or reference in your call does not exist. Please make sure ' \
              'that the collection name you are using is correct.'


class ErrorTransactionDataInvalidCollectionName(Exception):
    """
    DotMailer Exception: ERROR_TRANSACTIONAL_DATA_INVALID_COLLECTION_NAME
    """
    message = 'The transactional data collection name you are trying to ' \
              'create isn\'t valid. Valid transactional data collection ' \
              'names can only contain alphanumeric characters (A-Z, a-z, ' \
              '0-9), dashes ( - ) and underscores ( _ ), they can\'t start ' \
              'with a number and they can\'t exceed 255 characters in ' \
              'length. Please make sure that the collection name you are ' \
              'creating is valid.'


class ErrorTemplateInvalid(Exception):
    """
    DotMailer Exception: ERROR_TEMPLATE_INVALID
    """
    message = 'The template is not valid. This means that there is ' \
              'something incorrect with the template object you are sending ' \
              'to the method/operation. Check that your template object is ' \
              'valid by checking the definition in the documentation.'


class ErrorTemplateNotFound(Exception):
    """
    DotMailer Exception: ERROR_TEMPLATE_NOT_FOUND
    """
    message = 'The template object could not be found within the account. ' \
              'Either it has been deleted or it is likely that you are ' \
              'using the incorrect ID number.'


class ErrorThemeInvalid(Exception):
    """
    DotMailer Exception: ERROR_THEME_INVALID
    """
    message = 'You are attempting to set up an account with an invalid ' \
              'theme. Please check that the theme is correct.'


class ErrorTransactionalDataDoesNotExist(Exception):
    """
    DotMailer Exception: ERROR_TRANSACTIONAL_DATA_DOES_NOT_EXIST
    """
    message = 'This piece of transactional data does not exist. Either it ' \
              'has been deleted or it is likely that you are using the ' \
              'incorrect collection name or key.'


class ErrorTransactionalDataStorageAllowanceExceeded(Exception):
    """
    DotMailer Exception: ERROR_TRANSACTIONAL_DATA_STORAGE_ALLOWANCE_EXCEEDED
    """
    message = 'You have exceeded your transactional data storage allowance.'


class ErrorTransactionalDataValidationFailed(Exception):
    """
    DotMailer Exception: ERROR_TRANSACTIONAL_DATA_VALIDATION_FAILED
    """
    message = 'The validation of the transactional data failed. This means ' \
              'that there is something incorrect with the transactional ' \
              'data object you are sending to the method/operation. Check ' \
              'that your transactional data object is valid by checking the ' \
              'definition in the documentation.'


class ErrorUnknown(Exception):
    """
    DotMailer Exception: ERROR_UNKNOWN
    """
    message = 'We don\'t know what went wrong. Please contact our support ' \
              'department if you require assistance.'


class ErrorUnknownAccount(Exception):
    """
    DotMailer Exception: ERROR_UNKNOWN_ACCOUNT
    """
    message = 'The account is unknown. This means you are trying to ' \
              'reference an account that isn’t recognised. Please contact ' \
              'our support department if you require assistance.'


class ErrorUseraccountUnknown(Exception):
    """
    DotMailer Exception: ERROR_USERACCOUNT_UNKNOWN
    """
    message = 'This user account is not known. Please check the details you ' \
              'are using are valid.'


class ErrorWeakPassword(Exception):
    """
    DotMailer Exception: ERROR_WEAK_PASSWORD
    """
    message = 'The password set for your API credentials is too weak.'
