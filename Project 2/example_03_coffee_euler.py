#!/usr/bin/env python3

'''
A set of tools for solving Newton's law of cooling, i.e.,

$\frac{d T(t)}{dt} = k \left(T_{env} - T(t) \right)$

...where values and units are defined below.

Within this module are functions to return the analytic solution of the heat
equation, numerically solve it, find the time to arrive at a certain
temperature, and visualize the results.

The following table sets the values and their units used throughout this code:

| Symbol | Units  | Value/Meaning                                            |
|--------|--------|----------------------------------------------------------|
|T(t)    | C or K | Surface temperature of body in question                  |
|T_init  | C or K | Initial temperature of body in question                  |
|T_env   | C or K | Temperature of the ambient environment                   |
|k       | 1/s    | Heat transfer coefficient                                |
|t       | s      | Time in seconds                                          |


'''

# Standard imports:
import numpy as np
import matplotlib.pyplot as plt

# Set the plot style
# (see https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
plt.style.use('fivethirtyeight')


def solve_temp(t, k=1/300., T_env=20, T_init=90):
    '''
    For a given scalar or array of times, `t`, return the analytic solution
    for Newton's law of cooling:

    $T(t)=T_env + \left( T(t=0) - T_{env} \right) e^{-kt}$

    ...where all values are defined in the docstring for this module.

    Parameters
    ==========
    t : Numpy array
        Array of times, in seconds, for which solution will be provided.


    Other Parameters
    ================
    k : float
        Heat transfer coefficient, defaults to 1/300. s^-1
    T_env : float
        Ambient environment temperature, defaults to 20°C.
    T_init : float
        Initial temperature of cooling object/mass, defaults to °C

    Returns
    =======
    temp : numpy array
        An array of temperatures corresponding to `t`.
    '''

    return T_env + (T_init - T_env) * np.exp(-k*t)


def time_to_temp(T_target, k=1/300., T_env=20, T_init=90):
    '''
    Given an initial temperature, `T_init`, an ambient temperature, `T_env`,
    and a cooling rate, return the time required to reach a target temperature,
    `T_target`.

    Parameters
    ==========
    T_target : scalar or numpy array
        Target temperature in °C.
    k : float, default=1/300.
        Heat transfer coefficient, defaults to 1/300. s^-1
    T_env : float, default=20
        Ambient environment temperature, defaults to 20°C.
    T_init : float, default=90
        Initial temperature of cooling object/mass, defaults to °C

    Returns
    =======
    t : scalar or numpy array
        Time in s to reach the target temperature(s).
    '''

    return (-1/k) * np.log((T_target - T_env)/(T_init - T_env))


def euler(dfx, f0, tstop=600., dt=1.0):
    '''
    Solve an Ordinary Differential Equation (ODE) via Euler's method.

    Given a time derivative function, `dfx`, and an intial condition, f0,
    perform an Euler method integration to obtain the solution of an ODE
    in time. The function solution, f(x), is returned.

    Parameters
    ----------
    dfx : function
        A function that accepts the current value of f(x) and returns the
        time derivative.
    f0 : float
        The initial condition of the ODE.
    tstop : float, default=600
        The stop time of the integration in seconds.
    dt : timestep, default=1
        The time step in seconds.
    '''

    # Create time array. We won't use that here, but will return it
    # to the caller for convenience.
    t = np.arange(0, tstop, dt)

    # Create container for the solution, set initial condition.
    fx = np.zeros(t.size)
    fx[0] = f0

    # Integrate forward:
    for i in range(1, t.size):
        fx[i] = fx[i-1] + dt * dfx(fx[i-1])

    return t, fx


def coffee_problem1(T_env=21.0):
    '''
    This function solves the following problem:

    A cup of coffee is 90°C and is too hot to drink. You like cream in
    your coffee and adding it will cool the coffee instantaneously
    by 5°C. The coffee needs to cool until 60°C before it is
    drinkable. When should you add the creamer to get the coffee drinkable
    fastest- right away, or once it is already cooled to 60°C?

    It does so by setting an arbitrary heat transfer constant and
    plotting the cooling curves over 10 minutes for the creamer case and
    non-creamer case. The time-to-60°C is marked for each case.
    The ambient temperature is set to 21°C.

    Finally, we consider the "smart" solution where we let the coffee
    sit until it cools to 65°C and then pour in the cream to get to 60°C.
    '''

    # Create an initial time array:
    t = np.arange(0, 10*60., 0.1)

    # Create temperature curves for our two cases:
    temp_nocrm = solve_temp(t, T_init=90, T_env=T_env)
    temp_cream = solve_temp(t, T_init=90 - 5, T_env=T_env)

    # Get time-to-drinkable:
    tcool_nocrm = time_to_temp(60., T_env=T_env, T_init=90)
    tcool_cream = time_to_temp(60., T_env=T_env, T_init=85)
    tcool_smart = time_to_temp(65., T_env=T_env, T_init=90)

    # Create a figure and axes object, set custom figure size:
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Plot Case 1: No Cream. Plot time-to-drinkable as vertical line that
    # has the same color as the matching time series line.
    # The label is set with an "f-string". More info on those here:
    # https://github.com/spacecataz/python_syntax/blob/main/primer06_strformat.md
    l1 = ax.plot(t, temp_nocrm, label='No Cream')
    ax.axvline(tcool_nocrm, ls='--', c=l1[0].get_color(), lw=1.5,
               label=f"Drinkable in {tcool_nocrm:.0f}s")
    # Set a vertical line for Case 3: Cream at 65°C.
    # Color matches "no cream" case above.
    ax.axvline(tcool_smart, ls=':', c=l1[0].get_color(), lw=1.5,
               label="Cream at 65$^{{\\circ}}C$: \n"
               + f"Drinkable in {tcool_smart:.0f}s")

    # Repeat for Case 2: Cream Added.
    l2 = ax.plot(t, temp_cream, label='Cream Added')
    ax.axvline(tcool_cream, ls='--', c=l2[0].get_color(), lw=1.5,
               label=f"Drinkable in {tcool_cream:.0f}s")

    # Polish things up a bit.
    # Axes labels:
    ax.set_xlabel('Time ($s$)')
    ax.set_ylabel('Coffee Temperature ($^{\\circ}C$)')
    # Title:
    ax.set_title('Adding Cream Makes Java Sippable Faster')
    # Put the legend in a good spot:
    ax.legend(loc='best')
    # Tighten up margins:
    fig.tight_layout()

    return fig


def coffee_problem2():
    '''
    This function solves the coffee problem, but this time assumes that we
    can't solve the differential equation and employ Euler's method.

    We'll compare to our analytical solution to get an order of accuracy.
    '''

    # Configure parameter space:
    k = 1/300.
    T_env = 21.0
    T_init = 90
    dt = 60.

    # Create a function that represents our diffyQ:
    def dTdt(T):
        return -k*(T - T_env)

    # Get numerical solution:
    t, temp_euler = euler(dTdt, T_init, dt=dt)

    # Get analytical solution:
    temp_anlyt = solve_temp(t, T_init=T_init, T_env=T_env)

    # Compare!
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(t, temp_anlyt, label='Analytic Solution')
    ax.plot(t, temp_euler, label="Euler's Method")

    # Polish things up a bit.
    ax.set_xlabel('Time ($s$)')
    ax.set_ylabel('Coffee Temperature ($^{\\circ}C$)')
    ax.set_title(f'Solving Cooling Equation with Euler ($\\Delta t =${dt}$s$)')
    ax.legend(loc='best')
    # Tighten up margins:
    fig.tight_layout()
    fig.savefig('./demo03_coffee_euler.png')

    # Now, check convergence:
    # Create an array of dt values to test, build empty error container.
    dt_all = np.linspace(0.001, 10., 500)
    errors = np.zeros(dt_all.size)

    for i, dt in enumerate(dt_all):
        # Get both euler and analytic solution:
        t, temp_euler = euler(dTdt, T_init, dt=dt)
        temp_anlyt = solve_temp(t, T_init=T_init, T_env=T_env)

        # Calculate and save error:
        errors[i] = np.abs(temp_anlyt[-1] - temp_euler[-1])

    # Plot error vs. dt on log-log axes:
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.loglog(dt_all, errors, label='1st Order Diff')
    ax.loglog(dt_all, errors, '.', label='1st Order Diff')
    ax.set_xlabel(r'$\Delta x$')
    ax.set_ylabel('Error = |Analytic - Numeric|')
    ax.set_title("Convergence of Euler vs. $\\Delta t$")
    fig.tight_layout()
    fig.savefig('demo03_euler_converge.png')
    
coffee_problem2()
