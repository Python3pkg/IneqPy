#!/usr/bin/env python

"""A PYTHON PACKAGE TO QUANTITATIVE ANALYSIS OF INEQUALITY.

Collection of estimators of a stratified sample associated to single
individuals, in this module are calculations as the mean, variance,
quasivariance, population variance of a stratified sample.
"""
import pandas as pd
import numpy as np

# TODO implementar L-moments
# def legendre_pol(x):
#     """
#     https://en.wikipedia.org/wiki/Legendre_polynomials
#     https://es.wikipedia.org/wiki/Polinomios_de_Legendre
#     https://en.wikipedia.org/wiki/Binomial_coefficient
#     http://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/lmoment.htm
#     """
#     return None


def _to_df(*args, **kwargs):
    if args != ():
        res = pd.DataFrame([*args]).T
    elif kwargs is not None:
        res = pd.DataFrame.from_dict(kwargs, orient='columns')
    return res


def _apply_to_df(func, df, x, weights, *args, **kwargs):
    """This function generlize main arguments as Series of a pd.Dataframe.

    Parameters
    ---------
    func : function
        Function to convert his arguments in Series of an Dataframe.
    df : pandas.Dataframe
        DataFrame whats contains the Series `x_name` and `w_name`
    x_name : str
        Name of the column in `df`
    weights_name : str
        Name of the column in `df

    Returns
    -------
    return : func return
        It's depends of func output type

    Notes
    -----


    TODO
    ----


    Examples
    --------

    """
    return func(df[x], df[weights], *args, **kwargs)


def cmoment(x, weights=None, order=2, param=None, ddof=0):
    """Calculate the central moment of `x` with respect to `param` of order `n`,
    given the weights `w`.

    Parameters
    ----------
    x : 1d-array
        Variable
    weights : 1d-array
        Weights
    order : int, optional
        Moment order, 2 by default (variance)
    param : int or array, optional
        Parameter for which the moment is calculated, the default is None,
        implies use the mean.
    ddof : int, optional
        Degree of freedom, zero by default.

    Returns
    -------

    Notes
    -----
    - The cmoment of order 1 is 0
    - The cmoment of order 2 is the variance.
    Source : https://en.wikipedia.org/wiki/Moment_(mathematics)

    TODO
    ----
    Implement: https://en.wikipedia.org/wiki/L-moment#cite_note-wang:96-6

    Examples
    --------
    """
    # return np.sum((x-c)^n*counts) / np.sum(counts)
    if param is None:
        param = xbar(x, weights)
    elif not isinstance(param, (np.ndarray, int, float)):
        raise NotImplementedError
    if weights is None:
        weights = np.repeat([1], len(x))
    return np.sum((x - param) ** order * weights) / (np.sum(weights) - ddof)


def stdmoment(x, weights=None, param=None, order=3, ddof=0):
    """Calculate the standardized moment of order `c` for the variable` x` with
    respect to `c`.

    Parameters
    ---------
    x : 1d-array
       Random Variable
    weights : 1d-array, optional
       Weights or probability
    order : int, optional
       Order of Moment, three by default
    param : int or float or array, optional
       Central trend, default is the mean.
    ddof : int, optional
        Degree of freedom.

    Returns
    -------
    stdmoment : float
       Returns the standardized `n` order moment.

    Notes
    -----

    Source:

    - https://en.wikipedia.org/wiki/Moment_(mathematics)#Significance_of_the_moments
    - https://en.wikipedia.org/wiki/Standardized_moment


    TODO
    ----
    It is the general case of the raw and central moments. Review
    implementation.

    Examples
    --------

    """
    if weights is None:
        weights = np.repeat([1], len(x))
    if param is None:
        param = xbar(x, weights)
    # m = np.subtract(x, c)
    # m = np.power(m, n) * w / np.sum(w)
    # m = np.sum(m)
    # m = np.divide(m, np.power(var(x, w, ddof=ddof), n / 2))
    # return m
    res = cmoment(x, weights, order, param=param, ddof=ddof)
    res /= var(x, weights, ddof=ddof) ** (order / 2)
    return res


def xbar(x, weights=None):
    """Calculate the mean of `x` given weights `w`.

    Parameters
    ----------
    x : 1d-array or pd.Series or pd.DataFrame
        Variable on which the mean is estimated
    w : 1d-array or pd.Series or pd.DataFrame, optional
        Weights of the `x` variable of a dimension

    Retruns
    -------
    xbar : 1d-array or pd.Series or float
    """
    return np.average(x, weights=weights, axis=0)

def var(x, weights=None, ddof=0):
    """Calculate the population variance of `x` given
    weights `w`, for a homogeneous population.


    Parameters
    ----------
    x : 1d-array or pd.Series or pd.DataFrame
        Variable on which the quasivariation is estimated
    w : 1d-array or pd.Series or pd.DataFrame
        Weights of the `x` variable of a dimension

    Retruns
    -------
    Shat2 : 1d-array or pd.Series or float
        Estimation of quasivariance of `x`

    Notes
    -----

    If stratificated sample must pass with groupby each strata.
    """
    if weights is None:
        weights = np.repeat([1], len(x))
    return cmoment(x, weights=weights, order=2, ddof=ddof)


def kurt(x, weights):
    """Calculate the asymmetry coefficient

    Parameters
    ---------
    x : 1d-array
    w : 1d-array

    Returns
    -------
    kurt : float
        Coeficiente de curtosis.

    Notes
    -----
    It is an alias of the standardized fourth-order moment.

    TODO
    ----

    Examples
    --------
    """
    return stdmoment(x=x, weights=weights, order=4)


def skew(x, weights):
    """Returns the asymmetry coefficient of a sample.

    Parameters
    ---------
    x : 1d-array
    w : 1d-array

    Returns
    -------
    skew : float

    Notes
    -----
    It is an alias of the standardized third-order moment.

    TODO
    ----

    Examples
    --------
    """
    return stdmoment(x=x, weights=weights, order=3)


def shat2_h(df, x='x', weights='w', group='h'):
    """Sample variance of `x_name`, calculated as the second-order central
    moment.

    Parameters
    ---------

    Returns
    -------

    Notes
    -----

    TODO
    ----

    Examples
    --------
    """
    def sd(df):
        x = df.loc[:, x].copy().values
        weights = np.repeat([1], len(df))
        return cmoment(x, weights, 2, param=xbar(x))
    return df.groupby(group).apply(sd)


def vhat_h(x='x', weights='w', group='h', df=None):
    """Data a DataFrame calculates the sample variance for each stratum. The
    objective of this function is to make it easy to calculate the moments of
    the distribution that follows an estimator, eg. Can be used to calculate
    the variance that follows the mean.

    Parameters
    ---------
    df : pandas.DataFrame
        Dataframe containing the series needed for the calculation
    w_name : str
        Name of the weights `w` in the DataFrame
    h_name : str
        Name of the stratum variable `h` in the DataFrame

    Returns
    -------
    vhat_h : pandas.Series
        A series with the values of the variance of each `h` stratum.

    Notes
    -----

    TODO
    ----
    Review improvements.

    Examples
    --------
    >>> # Computes the variance of the mean
    >>> data = pd.DataFrame(data=[renta, peso, estrato],
                            columns=["renta", "peso", "estrato"])
    >>> v = vhat_h(data,x_name='income')
    >>> v
    stratum
    1                700.917.728,64
    2              9.431.897.980,96
    3            317.865.839.789,10
    4            741.304.873.092,88
    5            535.275.436.859,10
    6            225.573.783.240,68
    7            142.048.272.010,63
    8             40.136.989.131,06
    9             18.501.808.022,56
    dtype: float64

    >>> # the value of de variance of the mean:
    >>> v_total = v.sum() / peso.sum() ** 2
    24662655225.947945
    """
    if df is None:
        df = _to_df(x=x, weights=weights, group=group)
        x = 'x'
        weights = 'weights'
        group = 'group'

    def v(df):
        """Calculate the variance of each stratum `h`

        Parameters
        ---------
        df : pandas.DataFrame
            Dataframe containing the data

        Returns
        -------
        vhat : float
            Value of the population variance for the stratum `h`

        Notes
        -----
        Source:
        .. math:: r'N_h ^2 \cdot fpc \cdot \frac{ \hatS ^2 _h }{n_h}'

        TODO
        ----

        Examples
        --------
        """
        xi = df[x].copy().values
        Nh = df[weights].sum()
        fpc = 1 - (len(df) / Nh)
        ddof = 1 if len(df) > 1 else 0
        shat2h = cmoment(x=xi, order=2, ddof=ddof)
        return (Nh ** 2) * fpc * shat2h / len(df)
    return df.groupby(group).apply(v)


def moment_h(x='x', weights='w', group='h', df=None, order=2):
    """Calculates the asymmetry of each `h` stratum.

    Parameters
    ----------
    df :
    x :
    weights :
    group :
    order :

    Returns
    -------


    TODO
    ----
    Review calculations, it does not appear to be correct.
    Attempt to make a generalization of vhat_h, for any estimator.

    .. warning:: Not Work!

    Examples
    --------

    """
    if df is None:
        df = _to_df(x=x, weights=weights, group=group)
        x = 'x'
        weights = 'weights'
        group = 'group'

    def mh(df):
        x = df.loc[:, x].copy().values
        weights = np.repeat([1], len(df))
        Nh = df.loc[:, weights].sum()
        fpc = 1 - (len(df) / Nh)
        ddof = 1 if len(df) > 1 else 0
        stdm = stdmoment(x=x, weights=weights, order=order, ddof=ddof)
        return (Nh ** order) * fpc * stdm / len(df)
    return df.groupby(group).apply(mh)

'''Inequality functions'''


def lorenz(income, weights, df=None):
    """This function compute the lorenz curve and returns a DF with two columns
    of axis x and y.

    Parameters
    ---------
    df : pandas.DataFrame
        A pandas.DataFrame thats contains data.

    income : str or 1d-array, optional
        Population or wights, if a DataFrame is passed then `x` shuold be a
        name of the column of DataFrame, else can pass a pandas.Series or array.

    weights : str or 1d-array
        Income, monetary variable, if a DataFrame is passed then `y`is a name
        of the series on this DataFrame, however, you can pass a pd.Series or
        np.array.


    Returns
    -------
    lorenz : pandas.Dataframe
        Lorenz distribution in a Dataframe with two columns, labeled x and y,
        thats corresponds to plots axis.



    Notes
    -----


    TODO
    ----


    Examples
    --------


    """

    if df is None:
        df = _to_df(income=income, weights=weights)
        income='income'
        weights='weights'
        df[income] = df.income * df.weights
        res = df.sort_values(by=weights).cumsum() / df.sum()
    else:
        df[income] = df[income] * df[weights]
        res = df.sort_values(by=weights).cumsum() / df.sum()
    return res


def gini(income='x', weights='w', df=None, sorted=False):
    """Calcula el indice de Gini,

    Parameters
    ---------
    df : pandas.DataFrame
        DataFrame that contains the data.

    income : str or np.array, optional
        Name of the monetary variable `x` in` df`

    weights : str or np.array, optional
        Name of the series containing the weights `x` in` df`

    sorted : bool, optional
        If the DataFrame is previously ordered by the variable `x`, it's must pass True, but False by default.

    Returns
    -------
    gini : float
        Gini Index Value.

    Notes
    -----
    The calculation is done following (discrete probability distribution):

    G = 1 - [∑_i^n f(y_i)·(S_{i-1} + S_i)]

    where:

    - y_i = Income
    - S_i = ∑_{j=1}^i y_i · f(y_i)

    .. seealso::

        - https://en.wikipedia.org/wiki/Gini_coefficient
        - CALCULATING INCOME DISTRIBUTION INDICES FROM MICRO-DATA - STEPHEN JENKINS

    TODO
    ----
    Implement statistical deviation calculation, VAR (GINI)
    Clear comments
    Rename output

    Examples
    --------

    """
    if df is None:
        df = _to_df(income=income, weights=weights)
        income = 'income'
        weights = 'weights'
    # if any(df[income] <= 0):
    #     stage = df.loc[df[income] <= 0].copy().sum()
    #     stage[income] = 0
    #     df = pd.concat([stage.to_frame().T, df.loc[df[income] > 0]], axis=0)
    if not sorted:
        df = df[[income, weights]].sort_values(income,
                                               ascending=True).copy()
    # another aproach
    # x = df[income]
    # f_x = df[weights]
    # f_x /= f_x.sum()
    # si = x * f_x
    # si = si.cumsum()
    # si_1 = si.shift(1)
    # sn = si.iloc[-1]
    # g = (1 - np.divide(np.sum(f_x * (si_1 + si)), sn))
    # return G, G2, G3, G4
    x = df[income]
    f_x = df[weights] / df[weights].sum()
    F_x = f_x.cumsum()
    mu = np.sum(x * f_x)
    cov = np.cov(x, F_x, rowvar=False, aweights=f_x)[0,1]
    g = 2 * cov / mu
    return g


def atk(income, weights=None, e=0.5, df=None):
    """Calculate the coefficient of atkinson

    Parameters
    ---------
    income :

    weights :

    e :

    df :


    Returns
    -------


    Notes
    -----

    .. seealso::

        Source: https://en.wikipedia.org/wiki/Atkinson_index

    TODO
    ----
    implement file:///Users/mmngreco/Downloads/10.2307@41788716.pdf

    Examples
    --------


    """
    if (income is None) and (df is None):
        raise ValueError('Must pass at least one of both `income` or `df`')
    # non-null condition
    if np.any(income <= 0):
        mask = income > 0
        income = income[mask]
        if weights is not None:
            weights = weights[mask]
    # more than one value
    if len(income) == 0:
        return 0

    N = len(income)  # observations

    if weights is None:
        weights = np.repeat(1, N)

    mu = xbar(income, weights)
    f_i = weights / sum(weights)  # density function

    # another aproach
    # e value condition
    # if e == 1:
    #     Ee = np.power(np.e, np.sum(f_i * np.log(income)))
    # elif (0 <= e) or (e < 1):
    #     Ee = np.power(np.sum(f_i * np.power(income, 1 - e)), 1 / (1 - e))
    # else:
    #     assert (e < 0) or (e > 1), "Not valid e value,  0 ≤ e ≤ 1"
    #     Ee = None
    #     return None
    #
    # atkinson = (mu - Ee) / mu
    if e == 1:
        atkinson = 1 - np.power(np.e, np.sum(f_i * np.log(income) - np.log(mu)))
    elif (0 <= e) or (e < 1):
        atkinson = 1 - np.power(np.sum(f_i * np.power(income / mu, 1 - e)),
                                1 / (1 - e))
    else:
        assert (e < 0) or (e > 1), "Not valid e value,  0 ≤ e ≤ 1"
        atkinson = None
    return atkinson


def atk_h(income, weights, group, df=None, e=0.5):
    """

    Parameters
    ---------
    income : str or np.array
        Income variable, you can pass name of variable in `df` or array-like
    weights : str or np.array
        probability or weights, you can pass name of variable in `df` or
        array-like
    groups : str or np.array
        stratum, name of stratum in `df` or array-like
    e : int, optional
        Value of epsilon parameter
    df : pd.DataFrame, optional
        DataFrame that's contains the previous data.

    Returns
    -------
    atkinson_by_group : float

    Notes
    -----

    See Also
    --------
    Source: https://en.wikipedia.org/wiki/Atkinson_index

    TODO
    ----


    Examples
    --------

    """
    # df = df.loc[df[x] > 0].copy()
    # df.loc[:, weights] /= df[weights].sum()
    if df is None:
        df = _to_df(income=income, weights=weights, group=group)
        income = 'income'
        weights = 'weights'
        group = 'group'
    N = len(df)

    def a_h(data):
        '''
        Funtion alias to calculate atk from a DataFrame
        '''
        if data is None:
            raise ValueError

        res = atk(income=data[income].values,
                  weights=data[weights].values,
                  e=e) * len(data) / N
        return res

    if df is not None:
        atk_by_group = df.groupby(group).apply(a_h)
        mu_by_group = df.groupby(group).apply(lambda dw: xbar(dw[income],
                                                              dw[weights]))

        return atk_by_group.sum() + atk(income=mu_by_group.values)
    else:
        raise NotImplementedError