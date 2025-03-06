# Define list of curve functions

# Linear:
def linear(x, a, b): 
    """Linear function: y = a + bx"""
    return a + b * x

# Quadratic:
def quadratic(x, a, b, c):
    """Quadratic function: y = a + bx + cx^2"""
    return a + b * x + c * x**2

# Cubic:
def cubic(x, a, b, c, d):
    """Cubic function: y = a + bx + cx^2 + dx^3"""
    return a + b * x + c * x**2 + d * x**3

# Quartic: 
def quartic(x, a, b, c, d, e):
    """Quartic function: y = a + bx + cx^2 + dx^3 + ex^4"""
    return a + b * x + c * x**2 + d * x**3 + e * x**4

# Placeholder for custom user-defined functions:
# def custom_fxn(x, a): # Add additional parameters (b, c, d, etc.) for however many terms used in your function.
#    """
#    Define your own function here. 
#    For example: Exponential: y = a^x
#    """
#    return formula # Example: a**x

# Dictionary to store functions
# UNCOMMENT LAST LINE IF USING CUSTOM FUNCTION
MODEL_FUNCTIONS = {
    "linear": linear,
    "quadratic": quadratic,
    "cubic": cubic,
    "quartic": quartic,
    #"custom": custom_fxn,
}