#!/usr/bin/env python3
"""
library.py -- the basis library.

Every entry defines a node ONCE and gives it two implementations that sit
side by side in the same block: the Python reference and the C body. Keeping
them adjacent is the point -- the conformance harness in compile_c.py is only
meaningful because there is exactly one place where a node's meaning is stated
twice and can therefore be checked against itself.

Numerical conventions are fixed so the two implementations can agree exactly:
  * quantiles use nearest-rank on an ascending sort (no interpolation)
  * std is the population standard deviation (divide by n)
  * every division, log and sqrt is guarded; no node may return NaN or raise
  * binary vector ops truncate to the shorter operand
"""
from __future__ import annotations

import math
from typing import Dict, List

from core import BOOL, REAL, VEC, Op, Registry

REGISTRY = Registry()
C_BODIES: Dict[str, str] = {}

EPS = 1e-12


def _op(name, inputs, output, c_fn, c_body, cost=1.0, doc=""):
    def deco(fn):
        REGISTRY.add(Op(name, tuple(inputs), output, fn, c_fn, cost, doc))
        if c_body:
            C_BODIES[c_fn] = c_body
        return fn

    return deco


def _f(x) -> float:
    """Total: every node returns a finite real or a finite vector."""
    if x is None:
        return 0.0
    if isinstance(x, bool):
        return 1.0 if x else 0.0
    x = float(x)
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return x


def _v(x) -> List[float]:
    return [_f(t) for t in x]


# ---------------------------------------------------------------- real -> real
@_op("neg", [REAL], REAL, "nv_neg", "double nv_neg(double a){return nv_fin(-a);}")
def _neg(a):
    return _f(-_f(a))


@_op("abs", [REAL], REAL, "nv_abs", "double nv_abs(double a){return nv_fin(fabs(a));}")
def _abs(a):
    return _f(abs(_f(a)))


@_op("sq", [REAL], REAL, "nv_sq", "double nv_sq(double a){return nv_fin(a*a);}")
def _sq(a):
    return _f(_f(a) * _f(a))


@_op("sqrt", [REAL], REAL, "nv_sqrt", "double nv_sqrt(double a){return nv_fin(sqrt(fabs(a)));}")
def _sqrt(a):
    return _f(math.sqrt(abs(_f(a))))


@_op("log1p", [REAL], REAL, "nv_log1p", "double nv_log1p(double a){return nv_fin(log1p(fabs(a)));}")
def _log1p(a):
    return _f(math.log1p(abs(_f(a))))


@_op("inv", [REAL], REAL, "nv_inv",
     "double nv_inv(double a){return nv_fin(fabs(a)<NV_EPS?0.0:1.0/a);}")
def _inv(a):
    a = _f(a)
    return 0.0 if abs(a) < EPS else _f(1.0 / a)


# --------------------------------------------------------- real, real -> real
@_op("add", [REAL, REAL], REAL, "nv_add", "double nv_add(double a,double b){return nv_fin(a+b);}")
def _add(a, b):
    return _f(_f(a) + _f(b))


@_op("sub", [REAL, REAL], REAL, "nv_sub", "double nv_sub(double a,double b){return nv_fin(a-b);}")
def _sub(a, b):
    return _f(_f(a) - _f(b))


@_op("mul", [REAL, REAL], REAL, "nv_mul", "double nv_mul(double a,double b){return nv_fin(a*b);}")
def _mul(a, b):
    return _f(_f(a) * _f(b))


@_op("div", [REAL, REAL], REAL, "nv_div",
     "double nv_div(double a,double b){return nv_fin(fabs(b)<NV_EPS?0.0:a/b);}")
def _div(a, b):
    b = _f(b)
    return 0.0 if abs(b) < EPS else _f(_f(a) / b)


@_op("min2", [REAL, REAL], REAL, "nv_min2", "double nv_min2(double a,double b){return a<b?a:b;}")
def _min2(a, b):
    return _f(min(_f(a), _f(b)))


@_op("max2", [REAL, REAL], REAL, "nv_max2", "double nv_max2(double a,double b){return a>b?a:b;}")
def _max2(a, b):
    return _f(max(_f(a), _f(b)))


# ---------------------------------------------------------------- vec -> real
_C_SORT = """
static int nv_cmp(const void*x,const void*y){double a=*(const double*)x,b=*(const double*)y;
  return a<b?-1:(a>b?1:0);}
static double* nv_sorted(nv_arena*ar,nv_vec v){double*p=nv_alloc(ar,v.n);
  for(int i=0;i<v.n;i++)p[i]=v.d[i]; qsort(p,v.n,sizeof(double),nv_cmp); return p;}
static double nv_quant(nv_arena*ar,nv_vec v,double q){ if(v.n==0)return 0.0;
  double*p=nv_sorted(ar,v); long k=(long)floor(q*(v.n-1)+0.5);
  if(k<0)k=0; if(k>v.n-1)k=v.n-1; return nv_fin(p[k]); }
"""


def _quant(v, q):
    v = _v(v)
    if not v:
        return 0.0
    p = sorted(v)
    k = int(math.floor(q * (len(p) - 1) + 0.5))
    return _f(p[max(0, min(len(p) - 1, k))])


@_op("count", [VEC], REAL, "nv_count", "double nv_count(nv_arena*ar,nv_vec v){(void)ar;return (double)v.n;}")
def _count(v):
    return float(len(v))


@_op("sum", [VEC], REAL, "nv_sum",
     "double nv_sum(nv_arena*ar,nv_vec v){(void)ar;double s=0;for(int i=0;i<v.n;i++)s+=v.d[i];return nv_fin(s);}")
def _sum(v):
    return _f(sum(_v(v)))


@_op("mean", [VEC], REAL, "nv_mean",
     "double nv_mean(nv_arena*ar,nv_vec v){if(v.n==0)return 0.0;return nv_fin(nv_sum(ar,v)/v.n);}")
def _mean(v):
    v = _v(v)
    return 0.0 if not v else _f(sum(v) / len(v))


@_op("std", [VEC], REAL, "nv_std",
     """double nv_std(nv_arena*ar,nv_vec v){if(v.n==0)return 0.0;double m=nv_mean(ar,v),s=0;
  for(int i=0;i<v.n;i++){double d=v.d[i]-m;s+=d*d;} return nv_fin(sqrt(s/v.n));}""")
def _std(v):
    v = _v(v)
    if not v:
        return 0.0
    m = sum(v) / len(v)
    # (x - m) ** 2 raises OverflowError on float extremes where (x-m)*(x-m)
    # quietly gives inf, which _f then flattens. The C side has no exception
    # path at all, so multiplication is the only form that keeps the two
    # implementations in step. tests/test_nodegraph.py pins this.
    acc = 0.0
    for x in v:
        d = x - m
        acc += d * d
    return _f(math.sqrt(_f(acc / len(v))))


@_op("vmax", [VEC], REAL, "nv_vmax",
     "double nv_vmax(nv_arena*ar,nv_vec v){(void)ar;if(v.n==0)return 0.0;double m=v.d[0];"
     "for(int i=1;i<v.n;i++)if(v.d[i]>m)m=v.d[i];return nv_fin(m);}")
def _vmax(v):
    v = _v(v)
    return 0.0 if not v else _f(max(v))


@_op("vmin", [VEC], REAL, "nv_vmin",
     "double nv_vmin(nv_arena*ar,nv_vec v){(void)ar;if(v.n==0)return 0.0;double m=v.d[0];"
     "for(int i=1;i<v.n;i++)if(v.d[i]<m)m=v.d[i];return nv_fin(m);}")
def _vmin(v):
    v = _v(v)
    return 0.0 if not v else _f(min(v))


@_op("median", [VEC], REAL, "nv_median", "double nv_median(nv_arena*ar,nv_vec v){return nv_quant(ar,v,0.5);}", cost=2.0)
def _median(v):
    return _quant(v, 0.5)


@_op("q10", [VEC], REAL, "nv_q10", "double nv_q10(nv_arena*ar,nv_vec v){return nv_quant(ar,v,0.10);}", cost=2.0)
def _q10(v):
    return _quant(v, 0.10)


@_op("q90", [VEC], REAL, "nv_q90", "double nv_q90(nv_arena*ar,nv_vec v){return nv_quant(ar,v,0.90);}", cost=2.0)
def _q90(v):
    return _quant(v, 0.90)


@_op("iqr", [VEC], REAL, "nv_iqr",
     "double nv_iqr(nv_arena*ar,nv_vec v){return nv_fin(nv_quant(ar,v,0.75)-nv_quant(ar,v,0.25));}", cost=2.0)
def _iqr(v):
    return _f(_quant(v, 0.75) - _quant(v, 0.25))


@_op("gini", [VEC], REAL, "nv_gini",
     """double nv_gini(nv_arena*ar,nv_vec v){ if(v.n==0)return 0.0;
  nv_vec a=nv_new(ar,v.n); for(int i=0;i<v.n;i++)a.d[i]=fabs(v.d[i]);
  double*p=nv_sorted(ar,a); double s=0,w=0;
  for(int i=0;i<a.n;i++){s+=p[i]; w+=(double)(i+1)*p[i];}
  if(s<NV_EPS)return 0.0; return nv_fin(2.0*w/(a.n*s)-((double)a.n+1.0)/a.n);}""", cost=3.0)
def _gini(v):
    a = sorted(abs(x) for x in _v(v))
    if not a:
        return 0.0
    s = sum(a)
    if s < EPS:
        return 0.0
    w = sum((i + 1) * x for i, x in enumerate(a))
    return _f(2.0 * w / (len(a) * s) - (len(a) + 1.0) / len(a))


@_op("entropy", [VEC], REAL, "nv_entropy",
     """double nv_entropy(nv_arena*ar,nv_vec v){(void)ar; double s=0;
  for(int i=0;i<v.n;i++)s+=fabs(v.d[i]); if(s<NV_EPS)return 0.0; double h=0;
  for(int i=0;i<v.n;i++){double p=fabs(v.d[i])/s; if(p>NV_EPS)h-=p*log(p);} return nv_fin(h);}""", cost=2.0)
def _entropy(v):
    a = [abs(x) for x in _v(v)]
    s = sum(a)
    if s < EPS:
        return 0.0
    return _f(-sum((x / s) * math.log(x / s) for x in a if x / s > EPS))


@_op("topmean", [VEC], REAL, "nv_topmean",
     """double nv_topmean(nv_arena*ar,nv_vec v){ if(v.n==0)return 0.0; double*p=nv_sorted(ar,v);
  int k=(int)(v.n/10); if(k<1)k=1; double s=0; for(int i=v.n-k;i<v.n;i++)s+=p[i];
  return nv_fin(s/k);}""", cost=2.0)
def _topmean(v):
    p = sorted(_v(v))
    if not p:
        return 0.0
    k = max(1, len(p) // 10)
    return _f(sum(p[-k:]) / k)


@_op("cv", [VEC], REAL, "nv_cv",
     "double nv_cv(nv_arena*ar,nv_vec v){double m=nv_mean(ar,v);"
     "return fabs(m)<NV_EPS?0.0:nv_fin(nv_std(ar,v)/m);}", cost=2.0)
def _cv(v):
    m = _mean(v)
    return 0.0 if abs(m) < EPS else _f(_std(v) / m)


@_op("skew", [VEC], REAL, "nv_skew",
     """double nv_skew(nv_arena*ar,nv_vec v){ if(v.n==0)return 0.0; double m=nv_mean(ar,v),
  sd=nv_std(ar,v); if(sd<NV_EPS)return 0.0; double s=0;
  for(int i=0;i<v.n;i++){double z=(v.d[i]-m)/sd; s+=z*z*z;} return nv_fin(s/v.n);}""", cost=2.0)
def _skew(v):
    v = _v(v)
    if not v:
        return 0.0
    m = sum(v) / len(v)
    sd = _std(v)
    if sd < EPS:
        return 0.0
    acc = 0.0
    for x in v:
        z = (x - m) / sd
        acc += z * z * z
    return _f(_f(acc) / len(v))


# ----------------------------------------------------------------- vec -> vec
@_op("sortdesc", [VEC], VEC, "nv_sortdesc",
     """nv_vec nv_sortdesc(nv_arena*ar,nv_vec v){ double*p=nv_sorted(ar,v); nv_vec r=nv_new(ar,v.n);
  for(int i=0;i<v.n;i++)r.d[i]=p[v.n-1-i]; return r;}""", cost=2.0)
def _sortdesc(v):
    return sorted(_v(v), reverse=True)


@_op("norm1", [VEC], VEC, "nv_norm1",
     """nv_vec nv_norm1(nv_arena*ar,nv_vec v){ double s=0; for(int i=0;i<v.n;i++)s+=fabs(v.d[i]);
  nv_vec r=nv_new(ar,v.n); if(s<NV_EPS){for(int i=0;i<v.n;i++)r.d[i]=0.0; return r;}
  for(int i=0;i<v.n;i++)r.d[i]=nv_fin(v.d[i]/s); return r;}""")
def _norm1(v):
    v = _v(v)
    s = sum(abs(x) for x in v)
    return [0.0] * len(v) if s < EPS else [_f(x / s) for x in v]


@_op("zscore", [VEC], VEC, "nv_zscore",
     """nv_vec nv_zscore(nv_arena*ar,nv_vec v){ double m=nv_mean(ar,v),sd=nv_std(ar,v);
  nv_vec r=nv_new(ar,v.n); for(int i=0;i<v.n;i++)r.d[i]=sd<NV_EPS?0.0:nv_fin((v.d[i]-m)/sd);
  return r;}""", cost=2.0)
def _zscore(v):
    v = _v(v)
    m = _mean(v)
    sd = _std(v)
    return [0.0] * len(v) if sd < EPS else [_f((x - m) / sd) for x in v]


@_op("vlog1p", [VEC], VEC, "nv_vlog1p",
     "nv_vec nv_vlog1p(nv_arena*ar,nv_vec v){nv_vec r=nv_new(ar,v.n);"
     "for(int i=0;i<v.n;i++)r.d[i]=nv_fin(log1p(fabs(v.d[i])));return r;}")
def _vlog1p(v):
    return [_f(math.log1p(abs(x))) for x in _v(v)]


@_op("vsq", [VEC], VEC, "nv_vsq",
     "nv_vec nv_vsq(nv_arena*ar,nv_vec v){nv_vec r=nv_new(ar,v.n);"
     "for(int i=0;i<v.n;i++)r.d[i]=nv_fin(v.d[i]*v.d[i]);return r;}")
def _vsq(v):
    return [_f(x * x) for x in _v(v)]


@_op("diff", [VEC], VEC, "nv_diff",
     """nv_vec nv_diff(nv_arena*ar,nv_vec v){ if(v.n<2){nv_vec z=nv_new(ar,1);z.d[0]=0.0;return z;}
  double*p=nv_sorted(ar,v); nv_vec r=nv_new(ar,v.n-1);
  for(int i=0;i+1<v.n;i++)r.d[i]=nv_fin(p[i+1]-p[i]); return r;}""", cost=2.0)
def _diff(v):
    p = sorted(_v(v))
    if len(p) < 2:
        return [0.0]
    return [_f(p[i + 1] - p[i]) for i in range(len(p) - 1)]


# ------------------------------------------------------------ vec, real -> vec
@_op("vscale", [VEC, REAL], VEC, "nv_vscale",
     "nv_vec nv_vscale(nv_arena*ar,nv_vec v,double a){nv_vec r=nv_new(ar,v.n);"
     "for(int i=0;i<v.n;i++)r.d[i]=nv_fin(v.d[i]*a);return r;}")
def _vscale(v, a):
    a = _f(a)
    return [_f(x * a) for x in _v(v)]


@_op("vshift", [VEC, REAL], VEC, "nv_vshift",
     "nv_vec nv_vshift(nv_arena*ar,nv_vec v,double a){nv_vec r=nv_new(ar,v.n);"
     "for(int i=0;i<v.n;i++)r.d[i]=nv_fin(v.d[i]-a);return r;}")
def _vshift(v, a):
    a = _f(a)
    return [_f(x - a) for x in _v(v)]


@_op("clipmax", [VEC, REAL], VEC, "nv_clipmax",
     "nv_vec nv_clipmax(nv_arena*ar,nv_vec v,double a){nv_vec r=nv_new(ar,v.n);"
     "for(int i=0;i<v.n;i++)r.d[i]=v.d[i]>a?a:v.d[i];return r;}")
def _clipmax(v, a):
    a = _f(a)
    return [min(x, a) for x in _v(v)]


# ------------------------------------------------------------- vec, vec -> vec
@_op("vadd", [VEC, VEC], VEC, "nv_vadd",
     "nv_vec nv_vadd(nv_arena*ar,nv_vec a,nv_vec b){int n=a.n<b.n?a.n:b.n;nv_vec r=nv_new(ar,n);"
     "for(int i=0;i<n;i++)r.d[i]=nv_fin(a.d[i]+b.d[i]);return r;}")
def _vadd(a, b):
    a, b = _v(a), _v(b)
    n = min(len(a), len(b))
    return [_f(a[i] + b[i]) for i in range(n)]


@_op("vmul", [VEC, VEC], VEC, "nv_vmul",
     "nv_vec nv_vmul(nv_arena*ar,nv_vec a,nv_vec b){int n=a.n<b.n?a.n:b.n;nv_vec r=nv_new(ar,n);"
     "for(int i=0;i<n;i++)r.d[i]=nv_fin(a.d[i]*b.d[i]);return r;}")
def _vmul(a, b):
    a, b = _v(a), _v(b)
    n = min(len(a), len(b))
    return [_f(a[i] * b[i]) for i in range(n)]


# ------------------------------------------------------------ vec, vec -> real
@_op("corr", [VEC, VEC], REAL, "nv_corr",
     """double nv_corr(nv_arena*ar,nv_vec a,nv_vec b){(void)ar; int n=a.n<b.n?a.n:b.n;
  if(n<2)return 0.0; double ma=0,mb=0; for(int i=0;i<n;i++){ma+=a.d[i];mb+=b.d[i];}
  ma/=n; mb/=n; double sa=0,sb=0,sab=0;
  for(int i=0;i<n;i++){double x=a.d[i]-ma,y=b.d[i]-mb; sa+=x*x; sb+=y*y; sab+=x*y;}
  if(sa<NV_EPS||sb<NV_EPS)return 0.0; return nv_fin(sab/sqrt(sa*sb));}""", cost=2.0)
def _corr(a, b):
    a, b = _v(a), _v(b)
    n = min(len(a), len(b))
    if n < 2:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = sum(a) / n, sum(b) / n
    sa = _f(sum((x - ma) * (x - ma) for x in a))
    sb = _f(sum((y - mb) * (y - mb) for y in b))
    sab = _f(sum((x - ma) * (y - mb) for x, y in zip(a, b)))
    if sa < EPS or sb < EPS:
        return 0.0
    den = _f(math.sqrt(_f(sa * sb)))
    return 0.0 if den < EPS else _f(sab / den)


# ------------------------------------------------------------------ predicates
@_op("gt", [REAL, REAL], BOOL, "nv_gt", "double nv_gt(double a,double b){return a>b?1.0:0.0;}")
def _gt(a, b):
    return _f(a) > _f(b)


@_op("lt", [REAL, REAL], BOOL, "nv_lt", "double nv_lt(double a,double b){return a<b?1.0:0.0;}")
def _lt(a, b):
    return _f(a) < _f(b)


@_op("and", [BOOL, BOOL], BOOL, "nv_and", "double nv_and(double a,double b){return (a!=0.0&&b!=0.0)?1.0:0.0;}")
def _and(a, b):
    return bool(a) and bool(b)


@_op("or", [BOOL, BOOL], BOOL, "nv_or", "double nv_or(double a,double b){return (a!=0.0||b!=0.0)?1.0:0.0;}")
def _or(a, b):
    return bool(a) or bool(b)


@_op("not", [BOOL], BOOL, "nv_not", "double nv_not(double a){return a==0.0?1.0:0.0;}")
def _not(a):
    return not bool(a)


@_op("ifelse", [BOOL, REAL, REAL], REAL, "nv_ifelse",
     "double nv_ifelse(double c,double a,double b){return c!=0.0?a:b;}")
def _ifelse(c, a, b):
    return _f(a) if bool(c) else _f(b)


C_PRELUDE = r"""
#include <math.h>
#include <stdlib.h>
#include <string.h>
#define NV_EPS 1e-12
typedef struct { double *d; int n; } nv_vec;
typedef struct { double *buf; long used, cap; } nv_arena;
static double nv_fin(double x){ if(isnan(x)||isinf(x)) return 0.0; return x; }
static double* nv_alloc(nv_arena*ar,int n){ if(ar->used+n>ar->cap) return ar->buf; /* saturating */
  double*p=ar->buf+ar->used; ar->used+=n; return p; }
static nv_vec nv_new(nv_arena*ar,int n){ nv_vec v; v.d=nv_alloc(ar,n<1?1:n); v.n=n; return v; }
""" + _C_SORT


def c_runtime() -> str:
    """The full C runtime: prelude plus every node body, in dependency order."""
    order = [
        "nv_count", "nv_sum", "nv_mean", "nv_std", "nv_vmax", "nv_vmin",
        "nv_median", "nv_q10", "nv_q90", "nv_iqr", "nv_gini", "nv_entropy",
        "nv_topmean", "nv_cv", "nv_skew",
        "nv_sortdesc", "nv_norm1", "nv_zscore", "nv_vlog1p", "nv_vsq", "nv_diff",
        "nv_vscale", "nv_vshift", "nv_clipmax", "nv_vadd", "nv_vmul", "nv_corr",
    ]
    rest = [k for k in C_BODIES if k not in order]
    parts = [C_PRELUDE]
    for k in rest + order:
        parts.append(C_BODIES[k])
    return "\n".join(parts)
