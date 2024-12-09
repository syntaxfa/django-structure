# Rich Error

Rich Error is an error management pattern in programming that allows you to store detailed information about errors and the various layers in which these errors occurred before reaching you. Based on the collected information, you can easily display appropriate error messages to users or other systems.

Unlike standard errors, which typically include just a message or error code, Rich Error can include additional information such as metadata, the operation that caused the error, lower-level errors, and any other relevant details.

## Why Do We Call It Rich Error?

1. **More Information**:  
   Rich Error can include the error message, error code, the name of the operation that caused the error, and any other type of information. This information can include metadata that helps in better understanding the issue.

2. **Nested Structure**:  
   Rich Error allows you to manage nested errors. This means that if an error is caused by another error, you can trace back to the root cause, ensuring that no error is overlooked.

3. **Simplifies Your Work**:  
   As demonstrated in the examples, Rich Error simplifies your tasks and makes your code more organized and cohesive.

If you’re still uncertain about using Rich Error, here are some additional benefits:

1. **Better Problem Diagnosis**:  
   With rich information about errors, development teams can identify and resolve issues faster and more accurately.

2. **Enhanced User Experience**:  
   When errors are presented clearly with sufficient information, the user experience improves significantly.

3. **Faster Development**:  
   Using Rich Error can accelerate your development process, based on my own experience.

4. **Compatibility with Other Systems**:  
   The structured and sufficient information provided by Rich Error can be easily transferred to other systems. For example, you can utilize Rich Error information in your logging systems.
   
## How to Write a Rich Error?

One of the best ways to address such questions is to see how more experienced individuals have implemented this and what recommendations they provide.

The Microsoft documentation, particularly in the ErrorDetail section of the API guidelines, offers valuable insights. A Rich Error can include several key properties that help you store comprehensive information about errors. Below is a concise explanation of each property.
https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md

1. **operation**  
   This indicates the operation in which the error occurred. For example, it could be the name of the method or function that led to the error.
   - **Best Practice**: 
     - Use descriptive naming for the operation to make it easily identifiable.
     - This property can help you quickly identify issues in logs and reports.  
     For example, if the function `get_user_by_id` is in the `user` package and the `crud` file, and the error occurs within this package, the operation value could be:
     ```python
     RichError(operation="user.crud.get_user_by_id")
     ```

2. **code**  
   This property represents the error code, which is usually a number or a specific identifier. This code specifically references the type of error and can be used for categorizing errors.
   - **Best Practice**: 
     - Based on my experience, use a dictionary to manage error codes easily. 
     - Codes should be unique and meaningful for easy identification and management.

   **Why Should Error Codes Be Unique?**  
   This approach can help in error management. The idea is that each type of error should have a unique code that is easily identifiable and categorizable.

   **Benefits of Using Unique Error Codes**:
   1. **Quick Error Identification**:  
      Each error code points to a specific type of issue, helping us quickly understand what kind of error occurred.
   2. **Error Categorization**:  
      With unique codes, you can easily categorize errors based on type or resource.
   3. **Better Guidance for Users**:  
      Providing error codes to users or support teams allows them to easily refer to documentation or resources related to that error.
   4. **Reduced Overlap**:  
      Having specific codes for each type of error reduces the chance of overlap between errors.

   **Example of Error Codes**:
   To implement these codes, you can use a dictionary or Enum. I prefer using a dictionary:
   ```python
   USER_NOT_FOUND = 40401
   INVALID_INPUT = 40001
   INTERNAL_SERVER_ERROR = 50001
   ACCESS_DENIED = 40301

   ERROR_TRANSLATION = {
       USER_NOT_FOUND: "User does not exist",
       INVALID_INPUT: "Invalid input",
       INTERNAL_SERVER_ERROR: "Internal server error",
       ACCESS_DENIED: "Access denied"
   }
   ```
   Using a dictionary, we can easily provide text descriptions for each error or even utilize i18n (I prefer that clients display the appropriate text in their desired language based on the code).

3. **message**  
   A message that describes what type of error occurred. This message typically provides users or developers with more information about the nature of the error.
   - **Best Practice**: 
     - Use clear and concise messages that are easy to understand.
     - Messages should differ based on the type of error and user access level (e.g., for end users, messages should be simpler without rich details).

4. **error**  
   This property may refer to the underlying error that led to the Rich Error. It could be an exception that provides more details about the issue.
   - **Best Practice**: 
     - Use this property to store nested errors, meaning if one error is caused by another, store it here.
     - Ensure that information related to the original error is stored completely and clearly.

5. **meta_data**  
   This property can include any additional information that may be useful for better understanding the issue. For example, it can contain information about the system state, user inputs, etc.
   - **Best Practice**: 
     - Use a dictionary to store metadata so that you can easily manage different types of data.
     - This information should be collected and analyzed based on the specific needs and context of the error.

## Now You're Familiar with Rich Error!

At this point, you have a solid understanding of Rich Error. Next, I will explain the `rich-error` package and how to use Rich Error effectively and efficiently.

The `rich-error` package supports all the features we discussed. Here are some key points to keep in mind when using the `rich-error` package:

1. **Align Your Codes with HTTP Codes**:  
   Try to make your error codes correspond to HTTP status codes. This way, your codes can easily be converted into HTTP error responses. For example, use codes like:
   ```python
   OK = 200_00
   USER_NOT_FOUND = 404_01
   USER_CONFLICT = 409_01
   ```
   The first three digits of the codes should match the HTTP codes, while the subsequent digits can be whatever you prefer. Typically, codes range from five to six digits. Depending on the size of your project, you might have more than 99 instances of a specific code like 404, but I believe two additional digits are usually sufficient.

2. **Include Useful Information**:  
   Make sure to include as much useful information as possible within the Rich Error to simplify debugging.

3. **Access Error Information Easily**:  
   You can easily access the information inside the error using the `get_error_info` function.

By following these guidelines, you can effectively implement and utilize Rich Error in your applications.


## Example Using Rich Error

Let's consider an example where our application handles requests using a structure where a handler processes requests via a service, and if necessary, the service interacts with a database using a repository.

### Types of Errors That May Occur

Several types of errors may occur during this process. An error could happen in the repository and be returned to the service, which may also encounter its own set of errors. Ultimately, the handler should provide an appropriate response to the user.

Using Rich Error allows us to maintain a good log of errors as well as present a suitable response to the user. Here's how the code structure looks:

### `codes.py`
```python
OK = 200_00
USER_NOT_FOUND = 404_01
USER_CONFLICT = 409_01
IP_BLOCKED = 403_01
TOO_MANY_REQUEST = 429_01
INTERNAL_SERVER_ERROR = 500_01

ERROR_TRANSLATION = {
    OK: "ok",
    USER_NOT_FOUND: "user does not exist",  # We can use i18n for error translations, but I prefer not to.
    INTERNAL_SERVER_ERROR: "unexpected error",
    USER_CONFLICT: "this user already exists",
    IP_BLOCKED: "IP blocked",
    TOO_MANY_REQUEST: "too many requests",
}
```

### `api.py`
```python
from typing import Dict
from rich_error.utils.http.response import BaseResponse
from rich_error.utils.http.response import base_response as base_res
from rich_error.utils.http.response import base_response_with_error as base_res_error
from examples.with_rich_error.codes import OK, ERROR_TRANSLATION

def base_response(result: Dict | None, status_code: int = 200) -> BaseResponse:
    return base_res(status_code=status_code, code=OK, result=result)

def base_response_with_error(error: Exception):
    return base_res_error(error=error, error_translation=ERROR_TRANSLATION, code_k=100)
```

### `repository.py`
```python
from examples.with_rich_error.codes import USER_NOT_FOUND
from rich_error.error import RichError

class UserRepository:
    Op = "example.web.repository.UserRepository."

    def get_user_by_id(self, user_id: int):
        op = self.Op + "get_user_by_id"
        raise RichError(op).set_msg("User with this ID %d not found" % user_id).set_code(USER_NOT_FOUND)

def get_user_repository():
    return UserRepository()
```

### `service.py`
```python
import random
from abc import ABC, abstractmethod
from logging import error
from examples.with_rich_error import codes
from examples.with_rich_error.repository import get_user_repository
from rich_error.error import RichError, get_error_info

class Repository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

class UserService:
    Op = "examples.web.service.UserService."

    def __init__(self, repo: Repository):
        self.repo = repo

    def get_user_by_id(self, user_id: int):
        op = self.Op + "get_user_by_id"
        meta = {"user_id": user_id}

        try:
            match random.randint(1, 5):
                case 1:
                    raise RichError(op).set_code(codes.USER_CONFLICT)
                case 2:
                    raise RichError(op).set_code(codes.TOO_MANY_REQUEST)
                case 3:
                    raise RichError(op).set_code(codes.IP_BLOCKED)
                case (4, 5):
                    return self.repo.get_user_by_id(user_id=user_id)

            return self.repo.get_user_by_id(user_id=user_id)
        except Exception as err:
            """
            Since we have used Rich Error throughout the system, we know that the lower layer has handled it,
            and we just need to propagate the error.
            """
            # log error self.logger.error(...)
            rich_err = RichError(op).set_error(err).set_meta(meta)
            error(msg=get_error_info(error=rich_err))
            raise rich_err

def get_user_service():
    return UserService(repo=get_user_repository())
```

### `handler.py`
```python
from examples.with_rich_error.service import get_user_service
from examples.with_rich_error.api import base_response_with_error, base_response

service = get_user_service()


def get_user_handler(user_id: int):
    try:
        return base_response(result=service.get_user_by_id(user_id=user_id))
    except Exception as err:
        return base_response_with_error(error=err)


if __name__ == "__main__":
    print(get_user_handler(user_id=1))
```

### error info:
```shell
ERROR:root:[{'Operation': 'examples.web.service.UserService.get_user_by_id', 'Code': 40401, 'Message': 'user with this id 1 not found', 'Meta': {'user_id': 1}}, {'Operation': 'example.web.repository.UserRepository.get_user_by_id', 'Code': 40401, 'Message': 'user with this id 1 not found', 'Meta': {}}]
```

By using Rich Error, we can log errors effectively and provide meaningful responses to users, enhancing both debugging and user experience.


## The Drawback of Not Using Rich Error

If we didn't use Rich Error, we would have to handle different errors using alternative solutions, such as defining specific exceptions for each error type. For example, we might write:

```python
class UserNotFoundErr(Exception):
    pass

class IpBlockedErr(Exception):
    pass

class TooManyRequestErr(Exception):
    pass

class UserConflictErr(Exception):
    pass
```

In the handler, we would also need to define these exceptions:

```python
from examples.without_rich_error.service import get_user_service
from examples.without_rich_error.exception import UserNotFoundErr, UserConflictErr, TooManyRequestErr, IpBlockedErr

service = get_user_service()

def get_user_handler(user_id: int):
    try:
        print(service.get_user_by_id(user_id=user_id))
    except UserNotFoundErr as err:
        print("User not found, code is 404:", err)
    except UserConflictErr as err:
        print("User conflict, code is 409:", err)
    except TooManyRequestErr as err:
        print("Too many requests, code is 429:", err)
    except IpBlockedErr as err:
        print("IP blocked, code is 403:", err)

if __name__ == "__main__":
    print(get_user_handler(user_id=1))
```

### Challenges with This Approach

1. **Increased Duplication**: As the number of exceptions grows, managing them becomes increasingly complex and leads to code duplication.
  
2. **Reduced Observability**: The system's ability to provide insights into errors diminishes. In contrast, using Rich Error allows us to capture all errors occurring at various layers, maintaining a comprehensive view of the error landscape.

By leveraging Rich Error, we can simplify error management, reduce duplication, and enhance the observability of our error handling mechanism.
