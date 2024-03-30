import json

# Sample JSON data
json_data = {
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/tools/python": {
            "post": {
                "summary": "Execute Python",
                "operationId": "execute_python_tools_python_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Item"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/calculator": {
            "post": {
                "summary": "Evaluate",
                "operationId": "evaluate_tools_calculator_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Expression"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/arxiv": {
            "get": {
                "summary": "Get Arxiv Article Information",
                "description": "Run Arxiv search and get the article meta information.",
                "operationId": "get_arxiv_article_information_tools_arxiv_get",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ArxivQuery"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/bing/image_search": {
            "get": {
                "summary": "Image Search",
                "operationId": "image_search_tools_bing_image_search_get",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/QueryItemV2"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/bing/searchv2": {
            "get": {
                "summary": "Bing Search V2",
                "operationId": "bing_search_v2_tools_bing_searchv2_get",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/QueryItemV2"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/bing/load_pagev2": {
            "get": {
                "summary": "Load Page V2",
                "operationId": "load_page_v2_tools_bing_load_pagev2_get",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PageItemV2"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/shell": {
            "post": {
                "summary": "Execute Shell Command",
                "operationId": "execute_shell_command_tools_shell_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ShellCommandModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ShellCommandResultModel"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/create_file": {
            "post": {
                "summary": "Create File",
                "operationId": "create_file_tools_ppt_create_file_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CreateFileModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/get_image": {
            "post": {
                "summary": "Get Image",
                "operationId": "get_image_tools_ppt_get_image_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/GetImageModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/add_first_page": {
            "post": {
                "summary": "Add First Page",
                "operationId": "add_first_page_tools_ppt_add_first_page_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AddFirstPageModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/add_text_page": {
            "post": {
                "summary": "Add Text Page",
                "operationId": "add_text_page_tools_ppt_add_text_page_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AddTextPageModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/add_text_image_page": {
            "post": {
                "summary": "Add Text Image Page",
                "operationId": "add_text_image_page_tools_ppt_add_text_image_page_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AddTextImagePageModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/ppt/submit_file": {
            "get": {
                "summary": "Submit File",
                "operationId": "submit_file_tools_ppt_submit_file_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/tools/database": {
            "post": {
                "summary": "Execute Sqlite",
                "operationId": "execute_sqlite_tools_database_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/SQLRequest"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/wolframalpha": {
            "post": {
                "summary": "Wolframalpha Query",
                "operationId": "wolframalpha_query_tools_wolframalpha_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/QueryItem"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/weather/query": {
            "get": {
                "summary": "Query Weather",
                "operationId": "query_weather_weather_query_get",
                "parameters": [
                    {
                        "name": "date",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "title": "Date"
                        }
                    },
                    {
                        "name": "city",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "title": "City"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/calendar/insert_event": {
            "post": {
                "summary": "Insert Event",
                "operationId": "insert_event_calendar_insert_event_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CalendarEvent"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/gmail/send": {
            "post": {
                "summary": "Send Test Email",
                "operationId": "send_test_email_gmail_send_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EmailSchema"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/gmail/list": {
            "get": {
                "summary": "List Recent Emails",
                "operationId": "list_recent_emails_gmail_list_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/tools/markdown/web2md": {
            "get": {
                "summary": "Get Web Md",
                "operationId": "get_web_md_tools_markdown_web2md_get",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/TargetPageModel"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/audio2text": {
            "post": {
                "summary": "Audio2Text",
                "operationId": "audio2text_tools_audio2text_post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_audio2text_tools_audio2text_post"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/image_caption": {
            "post": {
                "summary": "Image Search",
                "operationId": "image_search_tools_image_caption_post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "allOf": [
                                    {
                                        "$ref": "#/components/schemas/Body_image_search_tools_image_caption_post"
                                    }
                                ],
                                "title": "Body"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tools/translate": {
            "post": {
                "summary": "Translate",
                "operationId": "translate_tools_translate_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/TranslateRequest"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/TranslateResponse"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "AddFirstPageModel": {
                "properties": {
                    "title": {
                        "type": "string",
                        "title": "Title"
                    },
                    "subtitle": {
                        "type": "string",
                        "title": "Subtitle"
                    }
                },
                "type": "object",
                "required": [
                    "title",
                    "subtitle"
                ],
                "title": "AddFirstPageModel"
            },
            "AddTextImagePageModel": {
                "properties": {
                    "title": {
                        "type": "string",
                        "title": "Title"
                    },
                    "bullet_items": {
                        "type": "string",
                        "title": "Bullet Items"
                    },
                    "image": {
                        "type": "string",
                        "title": "Image"
                    }
                },
                "type": "object",
                "required": [
                    "title",
                    "bullet_items",
                    "image"
                ],
                "title": "AddTextImagePageModel"
            },
            "AddTextPageModel": {
                "properties": {
                    "title": {
                        "type": "string",
                        "title": "Title"
                    },
                    "bullet_items": {
                        "type": "string",
                        "title": "Bullet Items"
                    }
                },
                "type": "object",
                "required": [
                    "title",
                    "bullet_items"
                ],
                "title": "AddTextPageModel"
            },
            "ArxivQuery": {
                "properties": {
                    "query": {
                        "type": "string",
                        "title": "Query"
                    }
                },
                "type": "object",
                "required": [
                    "query"
                ],
                "title": "ArxivQuery"
            },
            "Body_audio2text_tools_audio2text_post": {
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "title": "File"
                    }
                },
                "type": "object",
                "required": [
                    "file"
                ],
                "title": "Body_audio2text_tools_audio2text_post"
            },
            "Body_image_search_tools_image_caption_post": {
                "properties": {
                    "query": {
                        "anyOf": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Query",
                        "default": "What's in this image?"
                    },
                    "url": {
                        "anyOf": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Url"
                    },
                    "image_file": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "binary"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Image File"
                    }
                },
                "type": "object",
                "title": "Body_image_search_tools_image_caption_post"
            },
            "CalendarEvent": {
                "properties": {
                    "summary": {
                        "type": "string",
                        "title": "Summary"
                    },
                    "location": {
                        "type": "string",
                        "title": "Location"
                    },
                    "description": {
                        "type": "string",
                        "title": "Description"
                    },
                    "start": {
                        "type": "object",
                        "title": "Start",
                        "example": {
                            "dateTime": "2023-07-31T15:00:00",
                            "timeZone": "Asia/Shanghai"
                        }
                    },
                    "end": {
                        "type": "object",
                        "title": "End",
                        "example": {
                            "dateTime": "2023-07-31T16:00:00",
                            "timeZone": "Asia/Shanghai"
                        }
                    }
                },
                "type": "object",
                "required": [
                    "summary",
                    "location",
                    "description",
                    "start",
                    "end"
                ],
                "title": "CalendarEvent"
            },
            "CreateFileModel": {
                "properties": {
                    "theme": {
                        "type": "string",
                        "title": "Theme"
                    }
                },
                "type": "object",
                "required": [
                    "theme"
                ],
                "title": "CreateFileModel"
            },
            "EmailSchema": {
                "properties": {
                    "from_email": {
                        "type": "string",
                        "title": "From Email"
                    },
                    "to_email": {
                        "type": "string",
                        "title": "To Email"
                    },
                    "subject": {
                        "type": "string",
                        "title": "Subject"
                    },
                    "content": {
                        "type": "string",
                        "title": "Content"
                    }
                },
                "type": "object",
                "required": [
                    "from_email",
                    "to_email",
                    "subject",
                    "content"
                ],
                "title": "EmailSchema"
            },
            "Expression": {
                "properties": {
                    "expression": {
                        "type": "string",
                        "title": "Expression"
                    }
                },
                "type": "object",
                "required": [
                    "expression"
                ],
                "title": "Expression"
            },
            "GetImageModel": {
                "properties": {
                    "keywords": {
                        "type": "string",
                        "title": "Keywords"
                    }
                },
                "type": "object",
                "required": [
                    "keywords"
                ],
                "title": "GetImageModel"
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        },
                        "type": "array",
                        "title": "Detail"
                    }
                },
                "type": "object",
                "title": "HTTPValidationError"
            },
            "Item": {
                "properties": {
                    "code": {
                        "type": "string",
                        "title": "Code"
                    }
                },
                "type": "object",
                "required": [
                    "code"
                ],
                "title": "Item"
            },
            "PageItemV2": {
                "properties": {
                    "url": {
                        "type": "string",
                        "title": "Url"
                    },
                    "query": {
                        "anyOf": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Query"
                    }
                },
                "type": "object",
                "required": [
                    "url"
                ],
                "title": "PageItemV2"
            },
            "QueryItem": {
                "properties": {
                    "query": {
                        "type": "string",
                        "title": "Query"
                    }
                },
                "type": "object",
                "required": [
                    "query"
                ],
                "title": "QueryItem"
            },
            "QueryItemV2": {
                "properties": {
                    "query": {
                        "type": "string",
                        "title": "Query"
                    },
                    "top_k": {
                        "anyOf": [
                            {
                                "type": "integer"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Top K"
                    }
                },
                "type": "object",
                "required": [
                    "query"
                ],
                "title": "QueryItemV2"
            },
            "SQLRequest": {
                "properties": {
                    "queries": {
                        "items": {
                            "type": "string"
                        },
                        "type": "array",
                        "title": "Queries"
                    }
                },
                "type": "object",
                "required": [
                    "queries"
                ],
                "title": "SQLRequest"
            },
            "ShellCommandModel": {
                "properties": {
                    "command": {
                        "type": "string",
                        "title": "Command"
                    }
                },
                "type": "object",
                "required": [
                    "command"
                ],
                "title": "ShellCommandModel"
            },
            "ShellCommandResultModel": {
                "properties": {
                    "stdout": {
                        "type": "string",
                        "title": "Stdout"
                    },
                    "stderr": {
                        "type": "string",
                        "title": "Stderr"
                    }
                },
                "type": "object",
                "required": [
                    "stdout",
                    "stderr"
                ],
                "title": "ShellCommandResultModel"
            },
            "TargetPageModel": {
                "properties": {
                    "url": {
                        "type": "string",
                        "title": "Url"
                    }
                },
                "type": "object",
                "required": [
                    "url"
                ],
                "title": "TargetPageModel"
            },
            "TranslateRequest": {
                "properties": {
                    "text": {
                        "type": "string",
                        "title": "Text"
                    },
                    "src_language": {
                        "type": "string",
                        "title": "Src Language"
                    },
                    "dest_language": {
                        "type": "string",
                        "title": "Dest Language"
                    }
                },
                "type": "object",
                "required": [
                    "text",
                    "src_language",
                    "dest_language"
                ],
                "title": "TranslateRequest"
            },
            "TranslateResponse": {
                "properties": {
                    "translated_text": {
                        "type": "string",
                        "title": "Translated Text"
                    }
                },
                "type": "object",
                "required": [
                    "translated_text"
                ],
                "title": "TranslateResponse"
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "integer"
                                }
                            ]
                        },
                        "type": "array",
                        "title": "Location"
                    },
                    "msg": {
                        "type": "string",
                        "title": "Message"
                    },
                    "type": {
                        "type": "string",
                        "title": "Error Type"
                    }
                },
                "type": "object",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "title": "ValidationError"
            }
        }
    }
}

json_data2 = {
  "openapi": "3.1.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {  
    "/tools/markdown/web2md": {
      "get": {
        "summary": "This API can only get the markdown formatting of a web page at a given url but can not do summary work.",
        "operationId": "get_web_md_tools_markdown_web2md_get",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/TargetPageModel"
              }
            }
          },
          "required": True
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/tools/bing/searchv2": {
      "get": {
        "summary": "Execute Bing Search - returns top web snippets related to the query. Avoid using complex filters like 'site:'. For detailed page content, further use the web browser tool.",
        "operationId": "bing_search_v2_tools_bing_searchv2_get",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/QueryItemV2"
              }
            }
          },
          "required": True
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/tools/bing/load_pagev2": {
      "get": {
        "summary": "Web browser tool for detailed content retrieval and specific information extraction from a target URL.In the case of Wikipedia, the number of tokens on such pages is often too large to load the entire page, so the 'query' parameter must be given to perform a similarity query to find the most relevant pieces of content. The 'query' parameter should be assigned with your task description to find the most relevant content of the web page.It is important that your 'query' must retain enough details about the task, such as time, location, quantity, and other information, to ensure that the results obtained are accurate enough.",
        "operationId": "load_page_v2_tools_bing_load_pagev2_get",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/PageItemV2"
              }
            }
          },
          "required": True
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/weather/query": {
      "get": {
        "summary": "Query Weather",
        "operationId": "query_weather_weather_query_get",
        "parameters": [
          {
            "name": "date",
            "in": "query",
            "required": True,
            "schema": {
              "type": "string",
              "title": "Date"
            }
          },
          {
            "name": "city",
            "in": "query",
            "required": True,
            "schema": {
              "type": "string",
              "title": "City"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/gmail/send": {
      "post": {
        "summary": "Send google Email",
        "operationId": "send_test_email_gmail_send_post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/EmailSchema"
              }
            }
          },
          "required": True
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/gmail/list": {
      "get": {
        "summary": "List Recent Emails from gmail",
        "operationId": "list_recent_emails_gmail_list_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/tools/audio2text": {
      "post": {
        "summary": "A tool that converts audio to natural language text",
        "operationId": "audio2text_tools_audio2text_post",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "$ref": "#/components/schemas/Body_audio2text_tools_audio2text_post"
              }
            }
          },
          "required": True
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/tools/image_caption": {
      "post": {
        "summary": "When the task is to question and answer based on local picture, you have to use the Image Caption tool, who can directly analyze picture to answer question and complete task. For local images you want to understand, you need to only give the image_file without url. It is crucial to provide the 'query' parameter, and its value must be the full content of the task itself.",
        "operationId": "image_search_tools_image_caption_post",
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "required": False,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": "What's in this image?",
              "title": "Query"
            }
          },
          {
            "name": "url",
            "in": "query",
            "required": False,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "Url"
            }
          }
        ],
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "allOf": [
                  {
                    "$ref": "#/components/schemas/Body_image_search_tools_image_caption_post"
                  }
                ],
                "title": "Body"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "AddFirstPageModel": {
        "properties": {
          "title": {
            "type": "string",
            "title": "Title"
          },
          "subtitle": {
            "type": "string",
            "title": "Subtitle"
          }
        },
        "type": "object",
        "required": [
          "title",
          "subtitle"
        ],
        "title": "AddFirstPageModel"
      },
      "AddTextImagePageModel": {
        "properties": {
          "title": {
            "type": "string",
            "title": "Title"
          },
          "bullet_items": {
            "type": "string",
            "title": "Bullet Items"
          },
          "image": {
            "type": "string",
            "title": "Image"
          }
        },
        "type": "object",
        "required": [
          "title",
          "bullet_items",
          "image"
        ],
        "title": "AddTextImagePageModel"
      },
      "AddTextPageModel": {
        "properties": {
          "title": {
            "type": "string",
            "title": "Title"
          },
          "bullet_items": {
            "type": "string",
            "title": "Bullet Items"
          }
        },
        "type": "object",
        "required": [
          "title",
          "bullet_items"
        ],
        "title": "AddTextPageModel"
      },
      "CalendarEvent": {
        "properties": {
          "summary": {
            "type": "string",
            "title": "Summary"
          },
          "location": {
            "type": "string",
            "title": "Location"
          },
          "description": {
            "type": "string",
            "title": "Description"
          },
          "start": {
            "type": "object",
            "title": "Start",
            "example": {
              "dateTime": "2023-07-31T15:00:00",
              "timeZone": "Asia/Shanghai"
            }
          },
          "end": {
            "type": "object",
            "title": "End",
            "example": {
              "dateTime": "2023-07-31T16:00:00",
              "timeZone": "Asia/Shanghai"
            }
          }
        },
        "type": "object",
        "required": [
          "summary",
          "location",
          "description",
          "start",
          "end"
        ],
        "title": "CalendarEvent"
      },
      "CreateFileModel": {
        "properties": {
          "theme": {
            "type": "string",
            "title": "Theme"
          }
        },
        "type": "object",
        "required": [
          "theme"
        ],
        "title": "CreateFileModel"
      },
      "EmailSchema": {
        "properties": {
          "from_email": {
            "type": "string",
            "title": "From Email"
          },
          "to_email": {
            "type": "string",
            "title": "To Email"
          },
          "subject": {
            "type": "string",
            "title": "Subject"
          },
          "content": {
            "type": "string",
            "title": "Content"
          }
        },
        "type": "object",
        "required": [
          "from_email",
          "to_email",
          "subject",
          "content"
        ],
        "title": "EmailSchema"
      },
      "Expression": {
        "properties": {
          "expression": {
            "type": "string",
            "title": "Expression"
          }
        },
        "type": "object",
        "required": [
          "expression"
        ],
        "title": "Expression"
      },
      "GetImageModel": {
        "properties": {
          "keywords": {
            "type": "string",
            "title": "Keywords"
          }
        },
        "type": "object",
        "required": [
          "keywords"
        ],
        "title": "GetImageModel"
      },
      "HTTPValidationError": {
        "properties": {
          "detail": {
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "type": "array",
            "title": "Detail"
          }
        },
        "type": "object",
        "title": "HTTPValidationError"
      },
      "Item": {
        "properties": {
          "code": {
            "type": "string",
            "title": "Code"
          }
        },
        "type": "object",
        "required": [
          "code"
        ],
        "title": "Item"
      },
      "PageItemV2": {
        "properties": {
          "url": {
            "type": "string",
            "title": "Url"
          },
          "query": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Query"
          }
        },
        "type": "object",
        "required": [
          "url"
        ],
        "title": "PageItemV2"
      },
      "QueryItem": {
        "properties": {
          "query": {
            "type": "string",
            "title": "Query"
          }
        },
        "type": "object",
        "required": [
          "query"
        ],
        "title": "QueryItem"
      },
      "Body_image_search_tools_image_caption_post": {
        "properties": {
          "image_file": {
            "anyOf": [
              {
                "type": "string",
                "format": "binary"
              },
              {
                "type": "null"
              }
            ],
            "title": "Image File"
          }
        },
        "type": "object",
        "title": "Body_image_search_tools_image_caption_post"
      },
      "Body_audio2text_tools_audio2text_post": {
        "properties": {
          "file": {
            "type": "string",
            "format": "binary",
            "title": "File"
          }
        },
        "type": "object",
        "required": [
          "file"
        ],
        "title": "Body_audio2text_tools_audio2text_post"
      },
      "QueryItemV2": {
        "properties": {
          "query": {
            "type": "string",
            "title": "Query"
          },
          "top_k": {
            "anyOf": [
              {
                "type": "integer"
              },
              {
                "type": "null"
              }
            ],
            "title": "Top K"
          }
        },
        "type": "object",
        "required": [
          "query"
        ],
        "title": "QueryItemV2"
      },
      "TargetPageModel": {
        "properties": {
          "url": {
            "type": "string",
            "title": "Url"
          }
        },
        "type": "object",
        "required": [
          "url"
        ],
        "title": "TargetPageModel"
      },      
      "SQLRequest": {
        "properties": {
          "queries": {
            "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Queries"
          }
        },
        "type": "object",
        "required": [
          "queries"
        ],
        "title": "SQLRequest"
      },
      "ShellCommandModel": {
        "properties": {
          "command": {
            "type": "string",
            "title": "Command"
          }
        },
        "type": "object",
        "required": [
          "command"
        ],
        "title": "ShellCommandModel"
      },
      "ShellCommandResultModel": {
        "properties": {
          "stdout": {
            "type": "string",
            "title": "Stdout"
          },
          "stderr": {
            "type": "string",
            "title": "Stderr"
          }
        },
        "type": "object",
        "required": [
          "stdout",
          "stderr"
        ],
        "title": "ShellCommandResultModel"
      },
      "ValidationError": {
        "properties": {
          "loc": {
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            },
            "type": "array",
            "title": "Location"
          },
          "msg": {
            "type": "string",
            "title": "Message"
          },
          "type": {
            "type": "string",
            "title": "Error Type"
          }
        },
        "type": "object",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "title": "ValidationError"
      },
      "ArxivQuery": {
        "properties": {
          "query": {
            "type": "string",
            "title": "Query"
          }
        },
        "type": "object",
        "required": [
          "query"
        ],
        "title": "ArxivQuery"
      }
      
    }
  }
}

def resolve_ref(json_data, ref):
    """Resolves a $ref to its actual definition in the given JSON data."""
    parts = ref.split('/')
    result = json_data
    for part in parts[1:]:  # Skip the first element as it's always '#'
        result = result[part]
    return result

def extract_types_from_schema_element(schema_element):
    """从schema元素中提取类型信息，处理anyOf和直接定义的类型。"""
    if 'type' in schema_element:
        return [schema_element['type']]
    elif 'anyOf' in schema_element:
        types = []
        for sub_element in schema_element['anyOf']:
            types.extend(extract_types_from_schema_element(sub_element))
        return types
    else:
        return ['unknown']

def extract_properties_from_schema(schema, json_data):
    """递归地从schema中提取属性和类型信息，处理allOf、anyOf和$ref。"""
    properties = {}
    required = schema.get('required', [])

    if 'allOf' in schema:
        for item in schema['allOf']:
            sub_properties, sub_required = extract_properties_from_schema(item, json_data)
            properties.update(sub_properties)
            required.extend(sub_required)
    elif '$ref' in schema:
        ref_schema = resolve_ref(json_data, schema['$ref'])
        properties, required = extract_properties_from_schema(ref_schema, json_data)
    else:
        properties = schema.get('properties', {})

    return properties, required

def extract_api_details(json_data, api_path):
    api_details = json_data['paths'][api_path]
    for method, details in api_details.items():
        summary = details['summary']
        parameters_information = []
        request_body_format = None
        
        # 提取直接定义的参数
        if 'parameters' in details:
            for param in details['parameters']:
                parameter_info = {
                    'name': param['name'],
                    'in': param['in'],
                    'required': param.get('required', False),
                    'type': param['schema']['type'] if 'schema' in param else 'unknown'
                }
                parameters_information.append(parameter_info)
        
        # 处理requestBody（如果存在）
        if 'requestBody' in details:
            request_body_format = list(details['requestBody']['content'].keys())[0]
            schema_info = details['requestBody']['content'][request_body_format]['schema']
            
            properties, required = extract_properties_from_schema(schema_info, json_data)
            
            for prop, prop_details in properties.items():
                types = extract_types_from_schema_element(prop_details)  # 提取参数可能的类型
                parameter_info = {
                    'name': prop,
                    'type': types,  # 参数可能有多种类型
                    'required': prop in required
                }
                parameters_information.append(parameter_info)

        api_details_dict = {
            'api_path': api_path,
            'method': method,
            'summary': summary,
            'parameters': parameters_information,
            'request_body_format': request_body_format
        }
        
        return api_details_dict

# 使用更新后的函数提取特定路径的API细节
api_path_with_anyOf = '/tools/bing/load_pagev2'  # 或其他API路径
print(extract_api_details(json_data2, api_path_with_anyOf))

# for key in json_data2["paths"].keys():
#     print(key)
    
#     if key in json_data["paths"]:
#         if 'get' in json_data["paths"][key]:
#             json_data["paths"][key]['get']['summary'] = json_data2["paths"][key]['get']['summary']
#         if 'post' in json_data["paths"][key]:
#             json_data["paths"][key]['post']['summary'] = json_data2["paths"][key]['post']['summary']

# with open('merged.json', 'w') as f:
#     json.dump(json_data, f, indent=4)