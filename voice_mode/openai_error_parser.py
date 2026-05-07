"""
OpenAI API error parser for clear user-friendly error messages.

This module parses OpenAI API errors and provides clear, actionable messages
for common issues like quota limits, authentication problems, and rate limits.
"""

import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class OpenAIErrorParser:
    """Parse OpenAI API errors and provide user-friendly messages."""

    # Error code mappings for OpenAI API
    ERROR_CODES = {
        'insufficient_quota': 'quota_exceeded',
        'invalid_api_key': 'auth_failed',
        'invalid_request_error': 'invalid_request',
        'rate_limit_error': 'rate_limit',
        'billing_hard_limit_reached': 'billing_limit',
        'access_terminated': 'access_terminated',
    }

    # User-friendly messages for each error type
    ERROR_MESSAGES = {
        'quota_exceeded': {
            'title': '💳 OpenAI Quota Exceeded',
            'message': 'Your OpenAI API quota has been exceeded.',
            'suggestion': 'Check your OpenAI account at https://platform.openai.com/usage to review your usage and billing limits. Consider adding funds or upgrading your plan.',
            'fallback': 'You can use local voice services (Parakeet/Supertonic Express) which don\'t require API credits.'
        },
        'auth_failed': {
            'title': '🔐 OpenAI Authentication Failed',
            'message': 'The OpenAI API key is invalid or missing.',
            'suggestion': 'Set your OPENAI_API_KEY environment variable with a valid key from https://platform.openai.com/api-keys',
            'fallback': 'You can use local voice services (Parakeet/Supertonic Express) without an API key.'
        },
        'rate_limit': {
            'title': '⏱️ OpenAI Rate Limit',
            'message': 'You\'ve hit the OpenAI API rate limit.',
            'suggestion': 'Wait a moment and try again, or reduce the frequency of requests.',
            'fallback': 'Local services (Parakeet/Supertonic Express) have no rate limits.'
        },
        'billing_limit': {
            'title': '💰 OpenAI Billing Limit Reached',
            'message': 'Your OpenAI account has reached its billing hard limit.',
            'suggestion': 'Visit https://platform.openai.com/account/billing to increase your spending limit.',
            'fallback': 'Switch to local voice services which have no billing limits.'
        },
        'access_terminated': {
            'title': '🚫 OpenAI Access Terminated',
            'message': 'Your OpenAI account access has been terminated.',
            'suggestion': 'Contact OpenAI support or create a new account if appropriate.',
            'fallback': 'Use local voice services (Parakeet/Supertonic Express) instead.'
        },
        'invalid_request': {
            'title': '❌ Invalid Request',
            'message': 'The request to OpenAI API was invalid.',
            'suggestion': 'This might be a bug. Please report it if it persists.',
            'fallback': 'Try using local services as an alternative.'
        }
    }

    @classmethod
    def parse_error(cls, exception: Exception, endpoint: str = "") -> Dict[str, str]:
        """
        Parse an OpenAI API exception and return user-friendly error information.

        Args:
            exception: The exception raised by OpenAI API
            endpoint: The endpoint that was being accessed

        Returns:
            Dict with 'title', 'message', 'suggestion', and 'fallback' keys
        """
        error_info = cls._extract_error_info(exception)
        error_type = cls._determine_error_type(error_info)

        # Get the appropriate message
        if error_type in cls.ERROR_MESSAGES:
            result = cls.ERROR_MESSAGES[error_type].copy()
        else:
            # Generic error fallback
            result = {
                'title': '⚠️ OpenAI API Error',
                'message': f"OpenAI API error: {error_info.get('message', str(exception))}",
                'suggestion': 'Check your API configuration and try again.',
                'fallback': 'Consider using local voice services as an alternative.'
            }

        # Add endpoint info if provided
        if endpoint:
            result['endpoint'] = endpoint

        # Add status code if available
        if error_info.get('status_code'):
            result['status_code'] = error_info['status_code']

        # Add raw error for debugging
        result['raw_error'] = str(exception)

        return result

    @classmethod
    def _extract_error_info(cls, exception: Exception) -> Dict:
        """Extract structured information from the exception."""
        info = {
            'message': str(exception),
            'type': type(exception).__name__
        }

        # Check for HTTP status code
        if hasattr(exception, 'response'):
            response = exception.response
            if hasattr(response, 'status_code'):
                info['status_code'] = response.status_code
            if hasattr(response, 'text'):
                info['response_text'] = response.text
            if hasattr(response, 'json'):
                try:
                    info['response_json'] = response.json()
                except:
                    pass

        # Check for OpenAI-specific error attributes
        if hasattr(exception, 'status_code'):
            info['status_code'] = exception.status_code
        if hasattr(exception, 'error'):
            if isinstance(exception.error, dict):
                info['error_dict'] = exception.error
                if 'code' in exception.error:
                    info['error_code'] = exception.error['code']
                if 'message' in exception.error:
                    info['error_message'] = exception.error['message']

        return info

    @classmethod
    def _determine_error_type(cls, error_info: Dict) -> str:
        """Determine the type of error based on the extracted information."""

        # Check status codes first
        status_code = error_info.get('status_code')
        if status_code:
            if status_code == 401:
                return 'auth_failed'
            elif status_code == 429:
                # Could be rate limit or quota
                message = error_info.get('message', '').lower()
                response_text = error_info.get('response_text', '').lower()
                error_message = error_info.get('error_message', '').lower()

                all_text = f"{message} {response_text} {error_message}"

                if 'quota' in all_text or 'insufficient_quota' in all_text:
                    return 'quota_exceeded'
                elif 'billing' in all_text:
                    return 'billing_limit'
                else:
                    return 'rate_limit'
            elif status_code == 403:
                message = error_info.get('message', '').lower()
                if 'terminated' in message:
                    return 'access_terminated'
                return 'auth_failed'

        # Check error codes
        error_code = error_info.get('error_code', '').lower()
        if error_code in cls.ERROR_CODES:
            return cls.ERROR_CODES[error_code]

        # Check message content
        message = error_info.get('message', '').lower()
        error_message = error_info.get('error_message', '').lower()
        all_messages = f"{message} {error_message}"

        if 'insufficient_quota' in all_messages or 'quota' in all_messages:
            return 'quota_exceeded'
        elif 'invalid' in all_messages and 'key' in all_messages:
            return 'auth_failed'
        elif 'unauthorized' in all_messages or 'authentication' in all_messages:
            return 'auth_failed'
        elif 'rate' in all_messages and 'limit' in all_messages:
            return 'rate_limit'
        elif 'billing' in all_messages:
            return 'billing_limit'
        elif 'terminated' in all_messages:
            return 'access_terminated'

        # Default to unknown
        return 'unknown'

    @classmethod
    def format_error_message(cls, error_dict: Dict[str, str], include_fallback: bool = True) -> str:
        """
        Format error information into a user-friendly message string.

        Args:
            error_dict: Dictionary from parse_error()
            include_fallback: Whether to include fallback suggestion

        Returns:
            Formatted error message string
        """
        lines = [
            error_dict['title'],
            "",
            error_dict['message'],
            "",
            f"💡 {error_dict['suggestion']}"
        ]

        if include_fallback and 'fallback' in error_dict:
            lines.extend(["", f"ℹ️ {error_dict['fallback']}"])

        if 'status_code' in error_dict:
            lines.append(f"\n[HTTP {error_dict['status_code']}]")

        return "\n".join(lines)
