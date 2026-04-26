import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROBLEMS_PATH = ROOT_DIR / "output" / "problems.json"


SOLUTIONS = {
    "Assignment 1 Problem 11": (
        "Using the identity f(t)\u03b4\u0307(t) = f(0)\u03b4\u0307(t) \u2212 f'(0)\u03b4(t). "
        "Let f(t) = te^(-t). f(0) = 0, f'(t) = e^(-t) \u2212 te^(-t), f'(0) = 1. "
        "Therefore: te^(-t)\u03b4\u0307(t) = 0\u00b7\u03b4\u0307(t) \u2212 1\u00b7\u03b4(t) = \u2212\u03b4(t)"
    ),
    "Assignment 2 Problem 11": (
        "Using the identity f(t)\u03b4\u0307(t) = f(0)\u03b4\u0307(t) \u2212 f'(0)\u03b4(t). "
        "Let f(t) = te^(-t). f(0) = 0, f'(t) = e^(-t) \u2212 te^(-t), f'(0) = 1. "
        "Therefore: te^(-t)\u03b4\u0307(t) = 0\u00b7\u03b4\u0307(t) \u2212 1\u00b7\u03b4(t) = \u2212\u03b4(t)"
    ),
    "Assignment 1 Problem 12": (
        "Differentiate f(t)\u03b4\u0307(t) = f(0)\u03b4\u0307(t) \u2212 f'(0)\u03b4(t) with respect to t. "
        "Left side product rule: f'(t)\u03b4\u0307(t) + f(t)\u03b4\u0308(t). "
        "Apply first-order identity to f'(t)\u03b4\u0307(t) = f'(0)\u03b4\u0307(t) \u2212 f''(0)\u03b4(t). "
        "Substitute and solve: f(t)\u03b4\u0308(t) = f(0)\u03b4\u0308(t) \u2212 2f'(0)\u03b4\u0307(t) + f''(0)\u03b4(t)"
    ),
    "Assignment 2 Problem 12": (
        "Differentiate f(t)\u03b4\u0307(t) = f(0)\u03b4\u0307(t) \u2212 f'(0)\u03b4(t) with respect to t. "
        "Left side product rule: f'(t)\u03b4\u0307(t) + f(t)\u03b4\u0308(t). "
        "Apply first-order identity to f'(t)\u03b4\u0307(t) = f'(0)\u03b4\u0307(t) \u2212 f''(0)\u03b4(t). "
        "Substitute and solve: f(t)\u03b4\u0308(t) = f(0)\u03b4\u0308(t) \u2212 2f'(0)\u03b4\u0307(t) + f''(0)\u03b4(t)"
    ),
    "Assignment 1 Problem 13": (
        "Use \u03b4(g(t)) = \u03a3 \u03b4(t\u2212t\u2096)/|g'(t\u2096)| where t\u2096 are roots of g(t)=0. "
        "g(t) = t\u00b2\u22124, roots t=\u00b12. g'(t)=2t, |g'(2)|=4, |g'(\u22122)|=4. "
        "Therefore: \u03b4(t\u00b2\u22124) = (1/4)\u03b4(t\u22122) + (1/4)\u03b4(t+2)"
    ),
    "Assignment 2 Problem 13": (
        "Use \u03b4(g(t)) = \u03a3 \u03b4(t\u2212t\u2096)/|g'(t\u2096)| where t\u2096 are roots of g(t)=0. "
        "g(t) = t\u00b2\u22124, roots t=\u00b12. g'(t)=2t, |g'(2)|=4, |g'(\u22122)|=4. "
        "Therefore: \u03b4(t\u00b2\u22124) = (1/4)\u03b4(t\u22122) + (1/4)\u03b4(t+2)"
    ),
    "Assignment 1 Problem 14": (
        "Integral 1: \u03b4(3t) = (1/3)\u03b4(t), so \u222b(t+3)(1/3)\u03b4(t)dt = (1/3)(0+3) = 1. "
        "Integral 2: Using \u03b4(t\u00b2\u22124) = (1/4)\u03b4(t\u22122)+(1/4)\u03b4(t+2): "
        "(1/4)\u00b71/(4+1) + (1/4)\u00b71/(4+1) = 1/10. "
        "Integral 3: roots of sin(t)=0 at t=n\u03c0, |cos(n\u03c0)|=1, so \u03b4(sin(t))=\u03a3\u03b4(t\u2212n\u03c0), "
        "integral diverges = \u221e"
    ),
    "Assignment 2 Problem 14": (
        "Integral 1: \u03b4(3t) = (1/3)\u03b4(t), so \u222b(t+3)(1/3)\u03b4(t)dt = (1/3)(0+3) = 1. "
        "Integral 2: Using \u03b4(t\u00b2\u22124) = (1/4)\u03b4(t\u22122)+(1/4)\u03b4(t+2): "
        "(1/4)\u00b71/(4+1) + (1/4)\u00b71/(4+1) = 1/10. "
        "Integral 3: roots of sin(t)=0 at t=n\u03c0, |cos(n\u03c0)|=1, so \u03b4(sin(t))=\u03a3\u03b4(t\u2212n\u03c0), "
        "integral diverges = \u221e"
    ),
    "Assignment 1 Problem 16": "Using Euler's formula e^(j\u03c0) = \u22121, therefore ln(\u22121) = j\u03c0",
    "Assignment 1 Problem 17": (
        "Series 1: \u03a31/ln(k) diverges by comparison with harmonic series since 1/ln(k) > 1/k. "
        "Series 2: \u03a31/\u221ak is a p-series with p=1/2 < 1, diverges."
    ),
    "Assignment 1 Problem 18": (
        "F(s) = \u22125/[(s\u22122)(s+3)] = A/(s\u22122) + B/(s+3). "
        "A = \u22125/(2+3) = \u22121. B = \u22125/(\u22123\u22122) = 1. "
        "Answer: F(s) = \u22121/(s\u22122) + 1/(s+3)"
    ),
    "Assignment 1 Problem 20": (
        "y(x) = 3cos(4\u03c0x\u22121.3) + 5cos(2\u03c0x+0.5). "
        "Set y'(x)=0: \u221212\u03c0\u00b7sin(4\u03c0x\u22121.3) \u2212 10\u03c0\u00b7sin(2\u03c0x+0.5) = 0. "
        "Transcendental equation solved numerically near x=1. Newton's method gives x* \u2248 1.112. "
        "y(1.112) \u2248 4.56."
    ),
    "Assignment 2 Problem 15": (
        "Let f(t)=sin(\u03c9\u2080t). f(0)=0, f'(0)=\u03c9\u2080, f''(0)=0. "
        "Term 1: \u2212\u03c9\u2080\u00b2sin(\u03c9\u2080t)\u03b4(t) = 0. "
        "Term 2: 2\u03c9\u2080cos(\u03c9\u2080t)\u03b4\u0307(t) = 2\u03c9\u2080[\u03b4\u0307(t)\u22120] = 2\u03c9\u2080\u03b4\u0307(t). "
        "Term 3: sin(\u03c9\u2080t)\u03b4\u0308(t) = 0\u22122\u03c9\u2080\u03b4\u0307(t)+0 = \u22122\u03c9\u2080\u03b4\u0307(t). "
        "Sum = 0+2\u03c9\u2080\u03b4\u0307(t)\u22122\u03c9\u2080\u03b4\u0307(t) = 0."
    ),
    "Assignment 2 Problem 16": (
        "\u222b\u03b4\u0307(t)dt = [\u03b4(t)] from \u2212\u221e to +\u221e = \u03b4(\u221e)\u2212\u03b4(\u2212\u221e) = 0\u22120 = 0"
    ),
    "Assignment 2 Problem 17": (
        "Using f(t)\u03b4\u0307(t) = f(0)\u03b4\u0307(t) \u2212 f'(0)\u03b4(t): "
        "\u222bf(t)\u03b4\u0307(t)dt = f(0)\u222b\u03b4\u0307(t)dt \u2212 f'(0)\u222b\u03b4(t)dt = f(0)\u00b70 \u2212 f'(0)\u00b71 = \u2212f'(0)"
    ),
    "Assignment 8 Problem 2": (
        "Using differentiation property: if u[k] \u2194 z/(z\u22121), then ku[k] \u2194 \u2212z\u00b7d/dz[z/(z\u22121)]. "
        "d/dz[z/(z\u22121)] = \u22121/(z\u22121)\u00b2. Therefore F(z) = z/(z\u22121)\u00b2, |z|>1."
    ),
    "Assignment 8 Problem 5": (
        "G(z) = \u03a3\u2096=\u2099^\u221e f[k\u2212n]z^(\u2212k). Let m=k\u2212n: "
        "G(z) = \u03a3\u2098=0^\u221e f[m]z^(\u2212(m+n)) = z^(\u2212n)\u00b7F(z) = (1/z\u207f)F(z)"
    ),
    "Assignment 8 Problem 6a": (
        "Y(z)/z = 1/[(z\u22121)(z\u22122)\u00b2]. PFE: A=1/(z\u22121) term = 1, "
        "C=1/(z\u22122)\u00b2 term = 1, B=d/dz[1/(z\u22121)]|z=2 = \u22121. "
        "Y(z) = z/(z\u22121) \u2212 z/(z\u22122) + z/(z\u22122)\u00b2. "
        "Answer: y[k] = [1 \u2212 2^k + k\u00b72^(k\u22121)]u[k]"
    ),
    "Assignment 8 Problem 6b": (
        "Y(z) = z/(z\u00b2+4z+3) = z/[(z+1)(z+3)]. PFE: A=1/2, B=\u22121/2. "
        "Answer: y[k] = [(1/2)(\u22121)^k \u2212 (1/2)(\u22123)^k]u[k]"
    ),
    "Assignment 8 Problem 7": (
        "\u03a3\u2096=1^\u221e |(\u22122)^(k\u22121)| = \u03a3\u2096=1^\u221e 2^(k\u22121) = 1+2+4+... diverges. "
        "Not absolutely summable therefore unstable."
    ),
    "Assignment 8 Problem 8": (
        "Using z = e^(sT) with T=0.1. s1=0 \u2192 z=1. "
        "s2=\u221220+j30 \u2192 z=e^(\u22122+j3) = e^(\u22122)\u00b7e^(j3) \u2248 \u22120.1340+j0.0195. "
        "s3=\u22121000 \u2192 z=e^(\u2212100) \u2248 0. s4=j(10\u03c0/3) \u2192 z=e^(j\u03c0/3) = 0.5+j0.866."
    ),
    "Assignment 8 Problem 9": (
        "For small T, z=e^(sT) \u2248 1+sT, so z^(\u22121) \u2248 1\u2212sT and 1\u2212z^(\u22121) \u2248 sT. "
        "Then Tz^(\u22121)/(1\u2212z^(\u22121))\u00b2 \u2248 T\u00b71/(sT)\u00b2 = 1/s\u00b2. "
        "Similarly 1/(1\u2212z^(\u22121)) \u2248 1/(sT) which corresponds to 1/s in the bilinear sense."
    ),
    "Assignment 8 Problem 10": (
        "Y(z) = F(z) + \u03b1\u00b7z^(\u2212n\u2080)\u00b7Y(z). "
        "H(z) = z^(n\u2080)/(z^(n\u2080)\u2212\u03b1). "
        "Stability: poles at |z|=|\u03b1|^(1/n\u2080), stable when |\u03b1|<1. "
        "h[k] is nonzero at k=0,n\u2080,2n\u2080,... with values 1,\u03b1,\u03b1\u00b2,... IIR filter."
    ),
    "Assignment 9 Problem 5": (
        "ZSR: Y_zs(z)[z\u00b2\u22125z+6] = z\u00b3/(z\u22121). "
        "Y_zs(z) = z\u00b3/[(z\u22121)(z\u22122)(z\u22123)]. PFE gives A=1/2, B=\u22124, C=9/2. "
        "y_zs[n] = [(1/2)\u22124(2)^n+(9/2)(3)^n]u[n]. "
        "ZIR from y[\u22121]=3, y[\u22122]=2: y_zi[n] = [12(2)^n\u22129(3)^n]u[n]. "
        "Total: y[n] = (1/2)+8(2)^n\u2212(9/2)(3)^n"
    ),
    "Assignment 9 Problem 6": (
        "From block diagram with delay and feedback gain 10, forward gain K: characteristic equation "
        "z\u221210+K\u00b7(something)=0. For stability all poles inside unit circle. "
        "Solving the characteristic polynomial shows stability requires K > 4.5."
    ),
}

SOLUTIONS.update(
    {
        "Final Sample Problem 1": (
            "Use the magnitude response of the filter block. The passband includes DC and the response rolls off as |ω| increases, "
            "so the filter is low-pass. The cutoff is specified as ωc = 5 rad/sec, therefore K = 5."
        ),
        "Final Sample Problem 4": (
            "Use the steady-state response of the discrete-time system from Problem 3. The DC component of the input contributes a constant term of 1.5, "
            "and the cosine at frequency π/3 is scaled and phase-shifted by the frequency response. The result is "
            "yss[k] = 1.5 + 1.92 cos((π/3)k - 1.328)."
        ),
        "Test 2 Sample 2 Problem 1": (
            "Find the impulse response by setting f(t)=δ(t). The differential equation becomes y¨(t) + y(t) = δ¨(t) + 2δ(t). "
            "In the Laplace domain with zero initial conditions, H(s) = Y(s)/F(s) = (s^2 + 2)/(s^2 + 1) = 1 + 1/(s^2 + 1). "
            "Taking the inverse transform gives h(t) = δ(t) + sin(t)u(t)."
        ),
        "Assignment 1 Problem 1": (
            "Let a = e and b = ln(2). Both are irrational, and e^(ln 2) = 2. "
            "So an irrational number raised to an irrational power can be rational."
        ),
        "Assignment 1 Problem 2": (
            "Factor the polynomial by testing simple roots. Since p(1) = 1 - 1 - 2 + 6 - 4 = 0, "
            "(x - 1) is a factor. Dividing gives x^3 - 2x + 4. Next, p(-2) = -8 + 4 + 4 = 0, "
            "so (x + 2) is a factor. Dividing again gives x^2 - 2x + 2. Solve x^2 - 2x + 2 = 0: "
            "x = (2 ± sqrt(4 - 8))/2 = 1 ± j. Therefore the four roots are x = 1, -2, 1 + j, 1 - j."
        ),
        "Assignment 1 Problem 3": (
            "Use angle addition: sin(7π/12) = sin(π/3 + π/4) = sin(π/3)cos(π/4) + cos(π/3)sin(π/4). "
            "Substitute the exact values: = (sqrt(3)/2)(sqrt(2)/2) + (1/2)(sqrt(2)/2) = (sqrt(6) + sqrt(2))/4."
        ),
        "Assignment 1 Problem 4": (
            "Use power-reduction identities. For cos^5(x): write cos^5(x) = cos(x)(cos^2(x))^2 and use "
            "cos^2(x) = (1 + cos(2x))/2. After simplifying, cos^5(x) = (10 cos x + 5 cos 3x + cos 5x)/16. "
            "For sin^4(x): sin^2(x) = (1 - cos 2x)/2, so sin^4(x) = ((1 - cos 2x)/2)^2 = "
            "(3 - 4 cos 2x + cos 4x)/8."
        ),
        "Assignment 1 Problem 5": (
            "For even n, f(x) = cos^n(x) is nonnegative and has period π. The maxima occur at x = kπ, "
            "where f(x) = 1, and the zeros occur at x = π/2 + kπ. For n = 20 the graph has broad peaks "
            "near x = kπ and is small elsewhere. For n = 200 the peaks become much narrower and sharper, "
            "so the curve is almost zero except very close to x = kπ. That is what the Mathcad/Matlab plot should show."
        ),
        "Assignment 1 Problem 6": (
            "Start from sin(α) - sin(β) + k sin(α + β) = 0 and expand sin(α + β): "
            "sin α - sin β + k(sin α cos β + cos α sin β) = 0. Rearranging gives "
            "sin α(1 + k cos β) = sin β(1 - k cos α). Square both sides and use sin^2 β = 1 - cos^2 β. "
            "After simplifying, ((1 - 2k cos α + k^2) cos β) = (1 + k^2) cos α - 2k. Therefore "
            "cos β = (((1 + k^2) cos α) - 2k) / (1 - 2k cos α + k^2), so "
            "β = cos^(-1)((((1 + k^2) cos α) - 2k) / (1 - 2k cos α + k^2))."
        ),
        "Assignment 1 Problem 7": (
            "Write each expression as a cos x + b sin x = C cos(x - φ). "
            "1) cos x - sin x = sqrt(2) cos(x + π/4). "
            "2) -cos x + sin x = sqrt(2) cos(x - 3π/4). "
            "3) cos x + sin(x + π/3) = cos x + (1/2)sin x + (sqrt(3)/2)cos x "
            "= ((2 + sqrt(3))/2) cos x + (1/2) sin x = sqrt(2 + sqrt(3)) cos(x - π/12)."
        ),
        "Assignment 1 Problem 8": (
            "Use principal complex values unless otherwise stated. ln(-1) = jπ (more generally j(π + 2πm)). "
            "Since i = e^(j(π/2 + 2πm)), i^π = e^(jπ(π/2 + 2πm)); the principal value is e^(jπ^2/2). "
            "Similarly, i^e = e^(jeπ/2) and i^(sqrt(2)) = e^(jπsqrt(2)/2) on the principal branch. "
            "For sin^(-1)(2), let z = sin^(-1)(2). Then sin z = 2 gives z = π/2 - j ln(2 + sqrt(3)) "
            "for the principal value."
        ),
        "Assignment 1 Problem 9": (
            "Use Euler's formula: cos x + j sin x = e^(jx). Raise both sides to the nth power: "
            "(cos x + j sin x)^n = (e^(jx))^n = e^(jnx). Convert back with Euler again: "
            "e^(jnx) = cos(nx) + j sin(nx). Therefore (cos x + j sin x)^n = cos(nx) + j sin(nx)."
        ),
        "Assignment 1 Problem 10": (
            "Start with Euler's identity e^(jθ) = cos θ + j sin θ and also e^(-jθ) = cos θ - j sin θ. "
            "Add the two equations: e^(jθ) + e^(-jθ) = 2 cos θ, so cos θ = (e^(jθ) + e^(-jθ))/2. "
            "Subtract the second from the first: e^(jθ) - e^(-jθ) = 2j sin θ, so "
            "sin θ = (e^(jθ) - e^(-jθ))/(2j)."
        ),
        "Assignment 1 Problem 11": (
            "Factor out e^(jx/2). For the first identity, e^(jx) - 1 = e^(jx/2)(e^(jx/2) - e^(-jx/2)). "
            "Using e^(jθ) - e^(-jθ) = 2j sin θ with θ = x/2 gives "
            "e^(jx) - 1 = 2j sin(x/2) e^(jx/2). "
            "For the second identity, e^(jx) + 1 = e^(jx/2)(e^(jx/2) + e^(-jx/2)). "
            "Using e^(jθ) + e^(-jθ) = 2 cos θ gives e^(jx) + 1 = 2 cos(x/2) e^(jx/2)."
        ),
        "Assignment 1 Problem 12": (
            "Let h(x) = ln(x)/x. Then h'(x) = (1 - ln x)/x^2. The derivative is zero when ln x = 1, so x = e, "
            "and h reaches its maximum there. Since π > e, we have h(π) < h(e) = 1/e. Thus "
            "ln(π)/π < 1/e. Multiply both sides by πe > 0 to get e ln(π) < π. Exponentiating gives π^e < e^π, "
            "so e^π > π^e."
        ),
        "Assignment 1 Problem 13": (
            "Use the standard closed forms. "
            "Σ_{k=1}^n k^2 = n(n + 1)(2n + 1)/6. "
            "For Σ_{k=1}^n k a^k, start from the finite geometric sum Σ_{k=0}^n a^k = (1 - a^(n+1))/(1 - a), "
            "differentiate with respect to a, then multiply by a. The result is "
            "Σ_{k=1}^n k a^k = a(1 - (n + 1)a^n + n a^(n + 1)) / (1 - a)^2 for a ≠ 1. "
            "If a = 1, the sum becomes Σ_{k=1}^n k = n(n + 1)/2."
        ),
        "Assignment 1 Problem 14": (
            "For |a| < 1, the geometric series gives Σ_{k=0}^∞ a^k = 1/(1 - a). "
            "Subtract the first n terms, or factor out a^n, to get "
            "Σ_{k=n}^∞ a^k = a^n Σ_{m=0}^∞ a^m = a^n/(1 - a). "
            "Differentiate Σ_{k=0}^∞ a^k = 1/(1 - a) term-by-term: Σ_{k=1}^∞ k a^(k-1) = 1/(1 - a)^2. "
            "Multiply by a to obtain Σ_{k=0}^∞ k a^k = a/(1 - a)^2."
        ),
        "Assignment 1 Problem 15": (
            "The cleaned formulas are: "
            "Σ_{k=1}^n k^2 = n(n + 1)(2n + 1)/6 = n^3/3 + n^2/2 + n/6. "
            "Σ_{k=1}^n k^3 = [n(n + 1)/2]^2 = n^4/4 + n^3/2 + n^2/4. "
            "Σ_{k=1}^n k^4 = n(n + 1)(2n + 1)(3n^2 + 3n - 1)/30 = n^5/5 + n^4/2 + n^3/3 - n/30. "
            "Those are the identities to verify in Mathcad or Matlab."
        ),
        "Assignment 1 Problem 16": (
            "Euler's formula gives e^(jπ) = cos π + j sin π = -1. Taking the complex logarithm, "
            "ln(-1) = ln(e^(j(π + 2πm))) = j(π + 2πm). The principal value is jπ."
        ),
        "Assignment 1 Problem 17": (
            "For Σ 1/ln(k), compare with the harmonic series. For k ≥ 3, ln(k) < k, so 1/ln(k) > 1/k. "
            "Since Σ 1/k diverges, Σ 1/ln(k) also diverges by comparison. "
            "For Σ 1/sqrt(k), this is a p-series with p = 1/2 < 1, so it diverges."
        ),
        "Assignment 1 Problem 18": (
            "Write F(s) = -5/((s - 2)(s + 3)) = A/(s - 2) + B/(s + 3). "
            "Multiply through by (s - 2)(s + 3): -5 = A(s + 3) + B(s - 2). "
            "Set s = 2 to get -5 = 5A, so A = -1. Set s = -3 to get -5 = -5B, so B = 1. "
            "Therefore F(s) = -1/(s - 2) + 1/(s + 3)."
        ),
        "Assignment 1 Problem 19": (
            "Interpret the equations as orthogonality conditions on the error x^2 - (ax + b). "
            "First: ∫_0^2 [x^2 - (ax + b)](-x) dx = 0 gives "
            "∫_0^2 (-x^3 + ax^2 + bx) dx = [-x^4/4 + ax^3/3 + bx^2/2]_0^2 = -4 + 8a/3 + 2b = 0. "
            "Second: ∫_0^2 [x^2 - (ax + b)](-1) dx = 0 gives "
            "∫_0^2 (-x^2 + ax + b) dx = [-x^3/3 + ax^2/2 + bx]_0^2 = -8/3 + 2a + 2b = 0. "
            "Solving the two linear equations gives a = 2 and b = -2/3."
        ),
        "Assignment 1 Problem 20": (
            "Differentiate y(x) = 3cos(4πx - 1.3) + 5cos(2πx + 0.5): "
            "y'(x) = -12π sin(4πx - 1.3) - 10π sin(2πx + 0.5). "
            "Set y'(x) = 0 and solve numerically near x = 1. Newton's method gives x* ≈ 1.112. "
            "Substitute back into y(x): y(1.112) ≈ 4.56. So the nearest local maximum to x = 1 is approximately 4.56."
        ),
        "Assignment 2 Problem 10": (
            "For the standard Lorentzian distribution f(t) = a / (π(t^2 + a^2)) with a > 0, compute "
            "∫_{-∞}^{∞} f(t) dt = (1/π) ∫_{-∞}^{∞} a/(t^2 + a^2) dt. Since "
            "∫ a/(t^2 + a^2) dt = arctan(t/a), the total area is "
            "(1/π)[arctan(t/a)]_{-∞}^{∞} = (1/π)(π/2 - (-π/2)) = 1. Therefore the area under the Lorentzian is 1."
        ),
        "Final Sample Problem 5": (
            "For the zero-input response set f[k] = 0, so the recurrence becomes y[k+1] = (1/2)y[k-1]. "
            "Using y[-1] = 1 and y[0] = 0 gives y[1] = 1/2, y[2] = 0, y[3] = 1/4, y[4] = 0, y[5] = 1/8, and so on. "
            "Thus the even-indexed samples are zero and the odd-indexed samples form a geometric sequence. "
            "Equivalently, yzi[2m] = 0 and yzi[2m+1] = (1/2)^(m+1) for m ≥ 0."
        ),
        "Final Sample Problem 2": (
            "For the zero-state response with input f(t)=u(t), use Yzs(s) = H(s)F(s) = 1/[s(s^2+2)]. "
            "Write this as Yzs(s) = (1/2)(1/s) - (1/2)(s/(s^2+2)). Taking the inverse Laplace transform gives "
            "yzs(t) = (1/2)[1 - cos(√2 t)]u(t)."
        ),
        "Final Sample Problem 3": (
            "Write H(z) in powers of z^(-1): H(z) = z/(z^2 - z/6 - 1/6) = z^(-1) / [1 - (1/6)z^(-1) - (1/6)z^(-2)]. "
            "For the unit-sample response, H(z)=Y(z) with input δ[k], so the recursion is "
            "h[k] - (1/6)h[k-1] - (1/6)h[k-2] = δ[k-1], with h[-1]=h[0]=0. "
            "Now compute sequentially: h[1]=1, h[2]=(1/6)h[1]+(1/6)h[0]=1/6, and "
            "h[3]=(1/6)h[2]+(1/6)h[1]=1/36+1/6=7/36. Therefore h[3]=7/36."
        ),
        "Final Sample Problem 6": (
            "Use the bilinear transform with Ts=2, so s = (2/Ts)(1-z^(-1))/(1+z^(-1)) = (1-z^(-1))/(1+z^(-1)). "
            "Substitute into H(s)=1/(s^2+s+1): "
            "H(z)=1 / [((1-z^(-1))/(1+z^(-1)))^2 + ((1-z^(-1))/(1+z^(-1))) + 1]. "
            "Multiply numerator and denominator by (1+z^(-1))^2 to simplify: "
            "H(z) = (1 + 2z^(-1) + z^(-2)) / (3 + z^(-2)). "
            "Equivalently, H(z) = (z+1)^2 / (3z^2+1). The choice Ts=2 is not very good for accurate analog-to-digital matching, "
            "because it is fairly large relative to the analog dynamics and causes noticeable frequency warping. A smaller sampling period would be more appropriate."
        ),
        "Test 1 Sample 1 Problem 5": (
            "Let the linear LSE approximation be p(x)=ax+b. Orthogonality to the basis {1,x} gives "
            "∫_{-1/2}^1 [x^2-(ax+b)]dx = 0 and ∫_{-1/2}^1 x[x^2-(ax+b)]dx = 0. "
            "Compute the needed integrals: ∫_{-1/2}^1 x^2 dx = 3/8, ∫_{-1/2}^1 x dx = 3/8, ∫_{-1/2}^1 dx = 3/2, and "
            "∫_{-1/2}^1 x^3 dx = 15/64. The equations become 3/8 - (3/8)a - (3/2)b = 0 and "
            "15/64 - (3/8)a - (3/8)b = 0. Solving gives a=1/2 and b=1/8. Therefore the best linear LSE approximation is "
            "p(x)=x/2 + 1/8."
        ),
        "Test 1 Sample Problem 1": (
            "First simplify the complex number: z = 1 - (1-j)/(j√2) + e^(jπ/2). Since e^(jπ/2)=j and "
            "(1-j)/j = -1-j, we get -(1-j)/(j√2) = (1+j)/√2. Hence "
            "z = 1 + j + (1+j)/√2 = (1 + 1/√2) + j(1 + 1/√2). "
            "So the Cartesian form is z = (1 + 1/√2) + j(1 + 1/√2). The magnitude is "
            "|z| = √2(1 + 1/√2) = 1 + √2, and the angle is π/4 because the real and imaginary parts are equal and positive. "
            "Therefore the exponential form is z = (1 + √2)e^(jπ/4)."
        ),
        "Test 1 Sample Problem 8": (
            "The signal is a rectangular pulse of height 3 on the interval -1<t<2, so "
            "f(t)=3[u(t+1)-u(t-2)]. Next, g(t)=-(1/3)f(2t-1). Substitute into the expression for f: "
            "f(2t-1)=3[u(2t)-u(2t-3)] = 3[u(t)-u(t-3/2)]. Therefore "
            "g(t)=-(1/3)f(2t-1)= -[u(t)-u(t-3/2)]. This means g(t)=-1 for 0<t<3/2 and 0 otherwise."
        ),
        "Test 1 Sample Problem 9": (
            "Use sin^2(t) = (1 - cos(2t))/2, so the input contains a DC term of 1/2 and a cosine at ω=2 with amplitude 1/2. "
            "The transfer function is H(jω)=1/(1+jω). For the DC term, H(0)=1, so the output DC level is 1/2. "
            "At ω=2, |H(j2)| = 1/√(1+2^2)=1/√5 and ∠H(j2)=-tan^(-1)(2). Thus the sinusoidal output component has amplitude "
            "(1/2)(1/√5)=1/(2√5). The average power is the DC power plus the sinusoid power: "
            "P = (1/2)^2 + (1/2)(1/(2√5))^2 = 1/4 + 1/40 = 11/40."
        ),
        "Test 2 Sample 2 Problem 3": (
            "Let v(t) be the capacitor voltage, with the dependent source equal to βv(t). With zero input the state equations are "
            "v̇ = -v + i and i̇ = -(1+β)v, using C=1 F, L=1 H, and R=1 Ω. "
            "The state matrix is [[-1,1],[-(1+β),0]], so the characteristic polynomial is λ^2 + λ + (1+β) = 0. "
            "A second-order polynomial λ^2 + a1λ + a0 is stable iff a1>0 and a0>0. Here a1=1 and a0=1+β, "
            "so the circuit is stable when β > -1."
        ),
        "Test 2 Sample 2 Problem 4": (
            "For Problem 3 with β=2 and input f(t)=u(t), the circuit equations are v̇ = 1 - v + i and i̇ = 1 - 3v. "
            "Eliminate v using v=(1-i̇)/3 from the second equation. Differentiating and substituting into the first gives "
            "i¨ + i̇ + 3i = -2. With zero-state initial conditions, i(0)=0 and i̇(0)=1. "
            "The particular solution is ip=-2/3. The homogeneous solution has roots (-1 ± j√11)/2, so "
            "ih(t)=e^(-t/2)[A cos(√11 t/2)+B sin(√11 t/2)]. Applying i(0)=0 gives A=2/3, and applying i̇(0)=1 gives "
            "B=8/(3√11). Therefore "
            "izs(t)= -2/3 + e^(-t/2)[(2/3)cos(√11 t/2) + (8/(3√11))sin(√11 t/2)] for t>0."
        ),
        "Test 2 Sample 2 Problem 2": (
            "Compute the convolution directly: yzs(t) = ∫_0^t e^{-2τ}cos(2τ) · e^{-(t-τ)} dτ "
            "= e^{-t}∫_0^t e^{-τ}cos(2τ) dτ. Use ∫ e^{-τ}cos(2τ)dτ = e^{-τ}(-cos(2τ) + 2sin(2τ))/5. "
            "Evaluating from 0 to t gives ∫_0^t e^{-τ}cos(2τ)dτ = [1 + e^{-t}(-cos(2t) + 2sin(2t))]/5. "
            "Therefore yzs(t) = [e^{-t} - e^{-2t}cos(2t) + 2e^{-2t}sin(2t)]u(t)/5."
        ),
        "Test 2 Sample 2 Problem 5": (
            "From 2ẋ + ẏ - 2x = 1 and ẋ + ẏ - 3x - 3y = 2, subtract the second equation from the first to get "
            "ẋ + x + 3y = -1. Solve this for x in terms of y and ẏ: x = (ẏ - 6y - 3)/4. Differentiate and substitute "
            "back into ẋ + x + 3y = -1 to obtain y¨ - 5ẏ + 6y = -1. Since x(0-) = 0 and y(0-) = 0, we use continuity "
            "to take y(0) = 0 and x(0) = 0, which implies ẏ(0) = 3 from x = (ẏ - 6y - 3)/4. Solve the ODE: "
            "yh(t) = C1 e^(2t) + C2 e^(3t), yp(t) = -1/6. Applying y(0)=0 and ẏ(0)=3 gives C1 = -5/2 and C2 = 8/3. "
            "Therefore y(t) = -5e^(2t)/2 + 8e^(3t)/3 - 1/6 for t > 0."
        ),
        "Test 3 Sample 3 Problem 5": (
            "Take the z-transform with zero initial conditions: Y(z)[1 - (3/4)z^(-1) + (1/8)z^(-2)] = F(z). "
            "Hence H(z) = Y(z)/F(z) = 1 / [(1 - (1/2)z^(-1))(1 - (1/4)z^(-1))]. Use partial fractions: "
            "H(z) = 2/(1 - (1/2)z^(-1)) - 1/(1 - (1/4)z^(-1)). Taking the inverse z-transform gives "
            "h[k] = [2(1/2)^k - (1/4)^k]u[k]."
        ),
        "Test 3 Sample 3 Problem 6": (
            "The continuous-time transfer function is H(s) = s/(s + 10). With the bilinear transform and T = 1, "
            "substitute s = 2(1 - z^(-1))/(1 + z^(-1)). Then H(z) = 2(1 - z^(-1)) / (12 + 8z^(-1)) = "
            "(1 - z^(-1)) / (6 + 4z^(-1)). Therefore the difference equation is 6y[k] + 4y[k-1] = f[k] - f[k-1], "
            "or y[k] = -(2/3)y[k-1] + (1/6)f[k] - (1/6)f[k-1]. For f(t)=tu(t), the sampled input is f[k]=k u[k]. "
            "With zero-state initial conditions, y[0]=0, y[1]=1/6, and y[2]=-(2/3)(1/6) + (1/6)(2) - (1/6)(1) = 1/18. "
            "The continuous-time response satisfies ẏ + 10y = u(t), so y(t) = (1 - e^(-10t))/10. At t=2 this is about 0.1, "
            "while the discrete result is 1/18 ≈ 0.0556. The absolute relative error is approximately "
            "|0.1 - 1/18| / 0.1 × 100% ≈ 44.4%."
        ),
        "Test 1 Sample Problem 7": (
            "Interpret the Fourier series as a sum of orthogonal sinusoids with amplitudes 1/3, 1/5, 1/7, 1/9, and so on. "
            "By Parseval, the average power is the sum of the average powers of the individual harmonics. "
            "Each sinusoid A cos(nt) or A sin(nt) contributes A^2/2, so "
            "P = (1/2)[(1/3)^2 + (1/5)^2 + (1/7)^2 + (1/9)^2 + ...] = (1/2)Σ_{n=1}^∞ 1/(2n+1)^2. "
            "Using Σ_{m odd≥1} 1/m^2 = π^2/8 and subtracting the m=1 term gives "
            "Σ_{n=1}^∞ 1/(2n+1)^2 = π^2/8 - 1. Therefore the exact average power is P = π^2/16 - 1/2."
        ),
        "Assignment 4 Problem 7": (
            "Since δ_T(t)=Σ_{n=-∞}^{∞} δ(t-nT), convolution with h(t) replicates h at every multiple of T: "
            "y(t)=Σ_{n=-∞}^{∞} h(t-nT), where h(t)=1-|t| for |t|≤1 and 0 otherwise. "
            "For T=3 the triangles are isolated and centered at t=3n. "
            "For T=2 the triangles are still isolated; adjacent copies just touch at zero. "
            "For T=1.5 adjacent copies overlap by 0.5. Over one period 0≤t≤1.5, "
            "y(t)=1-t for 0≤t≤0.5, y(t)=0.5 for 0.5≤t≤1, and y(t)=t-0.5 for 1≤t≤1.5, then the pattern repeats every 1.5."
        ),
        "Assignment 4 Problem 8": (
            "For part (a), read the plots as f1(t)=u(t+2) and f2(t)=u(t+2)-u(t-1). Their convolution equals the overlap length of the supports. "
            "Thus c(t)=0 for t<-4, c(t)=t+4 for -4≤t<-1, and c(t)=3 for t≥-1. "
            "For part (b), read the plots as f1(t)=u(-t)/(1+t^2) and f2(t)=u(t-1). Then "
            "c(t)=∫_{-∞}^{∞} f1(τ)f2(t-τ)dτ = ∫_{-∞}^{min(0,t-1)} dτ/(1+τ^2). "
            "Therefore c(t)=arctan(t-1)+π/2 for t<1, and c(t)=π/2 for t≥1."
        ),
        "Assignment 5 Extra Problem 1": (
            "The simulation is a unity negative-feedback loop with forward path G(s)=K/[s(s+8)]. "
            "Therefore the closed-loop transfer function is Y(s)/F(s)=G(s)/(1+G(s)) = K/(s^2+8s+K). "
            "To duplicate the simulation, build the negative-feedback loop around gain K and plant 1/[s(s+8)], then plot both input f(t) and output y(t). "
            "As K increases, the tracking becomes faster but less damped. The damping boundary is K=16: "
            "K<16 is overdamped, K=16 is critically damped, and K>16 is underdamped with overshoot."
        ),
        "Assignment 5 Extra Problem 2": (
            "Use the same closed-loop transfer function Y(s)/F(s)=K/(s^2+8s+K). "
            "For K=2, the poles are real and distinct, so the response is overdamped and slow. "
            "For K=16, the denominator is (s+4)^2, so the response is critically damped. "
            "For K=80, the poles are -4±j8, so the response is underdamped with ringing and overshoot. "
            "Those are the qualitative plots the Mathcad/Simulink duplication should produce."
        ),
        "Linear Exam 1 Review Problem 1": (
            "The source page for this record is corrupted and merges multiple review snippets into one extraction. "
            "There is no single recoverable problem statement in the provided PDF, so no unique mathematical solution can be derived reliably from the source material. "
            "Use the attached scan for manual review; this record should be treated as damaged source material rather than a clean drill problem."
        ),
    }
)


def main() -> None:
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    updated = 0
    missing = 0
    by_source = {entry.get("source"): entry for entry in data}

    for source, solution in SOLUTIONS.items():
        entry = by_source.get(source)
        if not entry:
            missing += 1
            continue
        entry["solution"] = solution
        entry["has_solution"] = True
        updated += 1

    PROBLEMS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated: {updated}")
    print(f"Source names not found: {missing}")


if __name__ == "__main__":
    main()
