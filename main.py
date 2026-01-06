import logging
import sys
from typing import Dict, Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path

# ---------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# Get the directory where your script is located
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "math_mcp.log"

# Or use a temp directory if you prefer:
# import tempfile
# LOG_FILE = Path(tempfile.gettempdir()) / "math_mcp.log"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger("MathMCP")

# ---------------------------------------------------------------------
# MCP App Initialization
# ---------------------------------------------------------------------

app = FastMCP(
    name="Mathematics-MCP",
    version="1.0.0"
)

# ---------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------

class TwoNumberOperation(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

class SingleNumberOperation(BaseModel):
    a: float = Field(..., description="Input number")

class PowerOperation(BaseModel):
    base: float
    exponent: float

# ---------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------

def success_response(operation: str, result: Any) -> Dict[str, Any]:
    return {
        "status": "success",
        "operation": operation,
        "result": result
    }

def error_response(operation: str, message: str) -> Dict[str, Any]:
    logger.error(f"{operation} failed: {message}")
    return {
        "status": "error",
        "operation": operation,
        "message": message
    }

# ---------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------

@app.tool()
def add(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Perform addition of two numbers provided in the `data` object.
    Args:
        data (TwoNumberOperation): An object containing two numbers `a` and `b` 
                                   to be added.
    Returns:
        Dict[str, Any]: A dictionary containing the operation name ("add") and 
                        the result of the addition if successful, or an error 
                        message if an exception occurs.
    Logs:
        Logs the operation and result in the format:
        "ADD | {data.a} + {data.b} = {result}"
    """

    try:
        result = data.a + data.b
        logger.info(f"ADD | {data.a} + {data.b} = {result}")
        return success_response("add", result)
    except Exception as e:
        return error_response("add", str(e))

@app.tool()
def subtract(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Perform subtraction of two numbers provided in the `data` object.
    Args:
        data (TwoNumberOperation): An object containing two numbers, `a` and `b`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation name ("subtract") 
        and the result of the subtraction if successful, or an error message 
        if an exception occurs.
    Logs:
        Logs the subtraction operation and its result in the format:
        "SUB | {data.a} - {data.b} = {result}".
    """

    try:
        result = data.a - data.b
        logger.info(f"SUB | {data.a} - {data.b} = {result}")
        return success_response("subtract", result)
    except Exception as e:
        return error_response("subtract", str(e))

@app.tool()
def multiply(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Perform multiplication of two numbers provided in the `data` object.
    Args:
        data (TwoNumberOperation): An object containing two numbers `a` and `b` 
                                   to be multiplied.
    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication 
                        operation or an error message in case of failure.
    Logs:
        Logs the multiplication operation in the format:
        "MUL | {data.a} * {data.b} = {result}"
    Exceptions:
        Catches any exceptions that occur during the operation and returns an 
        error response with the exception message.
    """

    try:
        result = data.a * data.b
        logger.info(f"MUL | {data.a} * {data.b} = {result}")
        return success_response("multiply", result)
    except Exception as e:
        return error_response("multiply", str(e))

@app.tool()
def divide(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Perform division of two numbers provided in the `TwoNumberOperation` object.
    Args:
        data (TwoNumberOperation): An object containing two numbers, `a` and `b`, 
                                   where `a` is the numerator and `b` is the denominator.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ZeroDivisionError: If the denominator (`b`) is zero.
    Notes:
        - Logs the division operation and its result.
        - Returns a success response if the operation is successful.
        - Returns an error response if an exception occurs.
    """

    try:
        if data.b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        result = data.a / data.b
        logger.info(f"DIV | {data.a} / {data.b} = {result}")
        return success_response("divide", result)
    except Exception as e:
        return error_response("divide", str(e))

@app.tool()
def modulus(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Calculate the modulus (remainder) of two numbers provided in the `data` object.
    Args:
        data (TwoNumberOperation): An object containing two numbers, `a` and `b`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result if successful, 
                        or an error message if an exception occurs.
    Raises:
        ZeroDivisionError: If the second number (`b`) is zero, as modulus by zero is not allowed.
    Logs:
        Logs the operation and result in the format "MOD | a % b = result" if successful.
    Example:
        data = TwoNumberOperation(a=10, b=3)
        result = modulus(data)
        # result -> {"status": "success", "operation": "modulus", "result": 1}
    """

    try:
        if data.b == 0:
            raise ZeroDivisionError("Modulus by zero is not allowed.")
        result = data.a % data.b
        logger.info(f"MOD | {data.a} % {data.b} = {result}")
        return success_response("modulus", result)
    except Exception as e:
        return error_response("modulus", str(e))

@app.tool()
def power(data: PowerOperation) -> Dict[str, Any]:
    """
    Calculate the power of a given base raised to a given exponent.
    Args:
        data (PowerOperation): An object containing the base and exponent values.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Logs:
        Logs the operation in the format "POW | base ^ exponent = result".
    Exceptions:
        Catches any exceptions during the calculation and returns an error response.
    """

    try:
        result = pow(data.base, data.exponent)
        logger.info(f"POW | {data.base} ^ {data.exponent} = {result}")
        return success_response("power", result)
    except Exception as e:
        return error_response("power", str(e))

@app.tool()
def square(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Calculate the square of a given number.
    Args:
        data (SingleNumberOperation): An object containing the number to be squared.
    Returns:
        Dict[str, Any]: A dictionary containing the operation name ("square") 
                        and the result of squaring the input number. 
                        In case of an error, returns an error response.
    Logs:
        Logs the operation and the result in the format "SQUARE | <input>^2 = <result>".
    Raises:
        Exception: If an error occurs during the calculation.
    """

    try:
        result = data.a ** 2
        logger.info(f"SQUARE | {data.a}^2 = {result}")
        return success_response("square", result)
    except Exception as e:
        return error_response("square", str(e))

@app.tool()
def sqrt(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Calculate the square root of a given number.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation name, result, 
                        and status of the operation.
    Raises:
        ValueError: If the input number `a` is negative.
    Notes:
        - Logs the operation and result using the logger.
        - Returns a success response if the operation is successful.
        - Returns an error response if an exception occurs.
    """

    try:
        if data.a < 0:
            raise ValueError("Square root of negative number is not allowed.")
        result = data.a ** 0.5
        logger.info(f"SQRT | √{data.a} = {result}")
        return success_response("sqrt", result)
    except Exception as e:
        return error_response("sqrt", str(e))

# ---------------------------------------------------------------------
# Server Bootstrap
# ---------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logger.info("Starting Mathematics MCP Server...")
        app.run()
    except KeyboardInterrupt:
        logger.info("Math MCP Server stopped by user.")
    except Exception as exc:
        logger.critical(f"Fatal startup error: {exc}", exc_info=True)