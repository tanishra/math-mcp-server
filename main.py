import logging
import sys
from typing import Dict, Any
import math

from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path

# Logging Configuration

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

# MCP App Initialization

app = FastMCP(
    name="Mathematics-MCP",
    version="1.0.0"
)

# Request / Response Models

class TwoNumberOperation(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

class SingleNumberOperation(BaseModel):
    a: float = Field(..., description="Input number")

class PowerOperation(BaseModel):
    base: float
    exponent: float

class ListOperation(BaseModel):
    numbers: list[float] = Field(..., description="List of numbers")

class AngleOperation(BaseModel):
    angle: float = Field(..., description="Angle in degrees")

class LogOperation(BaseModel):
    value: float = Field(..., description="Value to calculate logarithm")
    base: float = Field(default=10, description="Base of logarithm (default: 10)")

# Helper Utilities

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

# MCP Tools - Basic Operations

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

# MCP Tools - Advanced Operations

@app.tool()
def factorial(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Calculate the factorial of a given number.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If the input is negative or not an integer.
    Notes:
        - Only works with non-negative integers.
        - Logs the operation and result.
    """

    try:
        if data.a < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if data.a != int(data.a):
            raise ValueError("Factorial is only defined for integers.")
        result = math.factorial(int(data.a))
        logger.info(f"FACTORIAL | {int(data.a)}! = {result}")
        return success_response("factorial", result)
    except Exception as e:
        return error_response("factorial", str(e))

@app.tool()
def absolute(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Calculate the absolute value of a given number.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Returns the absolute (non-negative) value of the input.
        - Logs the operation and result.
    """

    try:
        result = abs(data.a)
        logger.info(f"ABS | |{data.a}| = {result}")
        return success_response("absolute", result)
    except Exception as e:
        return error_response("absolute", str(e))

@app.tool()
def logarithm(data: LogOperation) -> Dict[str, Any]:
    """
    Calculate the logarithm of a value with a specified base.
    Args:
        data (LogOperation): An object containing the value and base for logarithm.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If value is non-positive or base is invalid.
    Notes:
        - Default base is 10 (common logarithm).
        - Use base 'e' (2.718...) for natural logarithm.
        - Logs the operation and result.
    """

    try:
        if data.value <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        if data.base <= 0 or data.base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")
        
        result = math.log(data.value, data.base)
        logger.info(f"LOG | log_{data.base}({data.value}) = {result}")
        return success_response("logarithm", result)
    except Exception as e:
        return error_response("logarithm", str(e))

@app.tool()
def natural_log(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Calculate the natural logarithm (base e) of a given number.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If the input is non-positive.
    Notes:
        - Natural log uses base e (approximately 2.718).
        - Logs the operation and result.
    """

    try:
        if data.a <= 0:
            raise ValueError("Natural logarithm is only defined for positive numbers.")
        result = math.log(data.a)
        logger.info(f"LN | ln({data.a}) = {result}")
        return success_response("natural_log", result)
    except Exception as e:
        return error_response("natural_log", str(e))

@app.tool()
def sine(data: AngleOperation) -> Dict[str, Any]:
    """
    Calculate the sine of an angle in degrees.
    Args:
        data (AngleOperation): An object containing the angle in degrees.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Input angle should be in degrees (not radians).
        - Result is between -1 and 1.
        - Logs the operation and result.
    """

    try:
        radians = math.radians(data.angle)
        result = math.sin(radians)
        logger.info(f"SIN | sin({data.angle}°) = {result}")
        return success_response("sine", result)
    except Exception as e:
        return error_response("sine", str(e))

@app.tool()
def cosine(data: AngleOperation) -> Dict[str, Any]:
    """
    Calculate the cosine of an angle in degrees.
    Args:
        data (AngleOperation): An object containing the angle in degrees.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Input angle should be in degrees (not radians).
        - Result is between -1 and 1.
        - Logs the operation and result.
    """

    try:
        radians = math.radians(data.angle)
        result = math.cos(radians)
        logger.info(f"COS | cos({data.angle}°) = {result}")
        return success_response("cosine", result)
    except Exception as e:
        return error_response("cosine", str(e))

@app.tool()
def tangent(data: AngleOperation) -> Dict[str, Any]:
    """
    Calculate the tangent of an angle in degrees.
    Args:
        data (AngleOperation): An object containing the angle in degrees.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Input angle should be in degrees (not radians).
        - Undefined at 90°, 270°, etc. (will return very large values).
        - Logs the operation and result.
    """

    try:
        radians = math.radians(data.angle)
        result = math.tan(radians)
        logger.info(f"TAN | tan({data.angle}°) = {result}")
        return success_response("tangent", result)
    except Exception as e:
        return error_response("tangent", str(e))

@app.tool()
def gcd(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Calculate the Greatest Common Divisor (GCD) of two numbers.
    Args:
        data (TwoNumberOperation): An object containing two numbers, `a` and `b`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If inputs are not integers.
    Notes:
        - Both numbers must be integers.
        - Returns the largest number that divides both inputs.
        - Logs the operation and result.
    """

    try:
        if data.a != int(data.a) or data.b != int(data.b):
            raise ValueError("GCD is only defined for integers.")
        result = math.gcd(int(data.a), int(data.b))
        logger.info(f"GCD | gcd({int(data.a)}, {int(data.b)}) = {result}")
        return success_response("gcd", result)
    except Exception as e:
        return error_response("gcd", str(e))

@app.tool()
def lcm(data: TwoNumberOperation) -> Dict[str, Any]:
    """
    Calculate the Least Common Multiple (LCM) of two numbers.
    Args:
        data (TwoNumberOperation): An object containing two numbers, `a` and `b`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If inputs are not integers.
    Notes:
        - Both numbers must be integers.
        - Returns the smallest number that is divisible by both inputs.
        - Logs the operation and result.
    """

    try:
        if data.a != int(data.a) or data.b != int(data.b):
            raise ValueError("LCM is only defined for integers.")
        result = math.lcm(int(data.a), int(data.b))
        logger.info(f"LCM | lcm({int(data.a)}, {int(data.b)}) = {result}")
        return success_response("lcm", result)
    except Exception as e:
        return error_response("lcm", str(e))

@app.tool()
def mean(data: ListOperation) -> Dict[str, Any]:
    """
    Calculate the mean (average) of a list of numbers.
    Args:
        data (ListOperation): An object containing a list of numbers.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If the list is empty.
    Notes:
        - Mean is the sum of all numbers divided by count.
        - Logs the operation and result.
    """

    try:
        if not data.numbers:
            raise ValueError("Cannot calculate mean of an empty list.")
        result = sum(data.numbers) / len(data.numbers)
        logger.info(f"MEAN | mean({data.numbers}) = {result}")
        return success_response("mean", result)
    except Exception as e:
        return error_response("mean", str(e))

@app.tool()
def median(data: ListOperation) -> Dict[str, Any]:
    """
    Calculate the median of a list of numbers.
    Args:
        data (ListOperation): An object containing a list of numbers.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If the list is empty.
    Notes:
        - Median is the middle value when numbers are sorted.
        - For even-length lists, returns average of two middle values.
        - Logs the operation and result.
    """

    try:
        if not data.numbers:
            raise ValueError("Cannot calculate median of an empty list.")
        sorted_numbers = sorted(data.numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            result = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
        else:
            result = sorted_numbers[n // 2]
        logger.info(f"MEDIAN | median({data.numbers}) = {result}")
        return success_response("median", result)
    except Exception as e:
        return error_response("median", str(e))

@app.tool()
def standard_deviation(data: ListOperation) -> Dict[str, Any]:
    """
    Calculate the standard deviation of a list of numbers.
    Args:
        data (ListOperation): An object containing a list of numbers.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Raises:
        ValueError: If the list has fewer than 2 numbers.
    Notes:
        - Measures the amount of variation in the dataset.
        - Uses sample standard deviation (n-1 denominator).
        - Logs the operation and result.
    """

    try:
        if len(data.numbers) < 2:
            raise ValueError("Standard deviation requires at least 2 numbers.")
        mean_value = sum(data.numbers) / len(data.numbers)
        variance = sum((x - mean_value) ** 2 for x in data.numbers) / (len(data.numbers) - 1)
        result = math.sqrt(variance)
        logger.info(f"STDDEV | stddev({data.numbers}) = {result}")
        return success_response("standard_deviation", result)
    except Exception as e:
        return error_response("standard_deviation", str(e))

@app.tool()
def ceiling(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Round a number up to the nearest integer.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Always rounds up (e.g., 3.1 -> 4, -3.1 -> -3).
        - Logs the operation and result.
    """

    try:
        result = math.ceil(data.a)
        logger.info(f"CEIL | ceil({data.a}) = {result}")
        return success_response("ceiling", result)
    except Exception as e:
        return error_response("ceiling", str(e))

@app.tool()
def floor(data: SingleNumberOperation) -> Dict[str, Any]:
    """
    Round a number down to the nearest integer.
    Args:
        data (SingleNumberOperation): An object containing the input number `a`.
    Returns:
        Dict[str, Any]: A dictionary containing the operation result or an error message.
    Notes:
        - Always rounds down (e.g., 3.9 -> 3, -3.1 -> -4).
        - Logs the operation and result.
    """

    try:
        result = math.floor(data.a)
        logger.info(f"FLOOR | floor({data.a}) = {result}")
        return success_response("floor", result)
    except Exception as e:
        return error_response("floor", str(e))

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