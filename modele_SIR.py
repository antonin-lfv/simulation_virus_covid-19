# Import
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go

# Population 
N = 10000

# Nombre initial de sujets infectés et 'removed' (immunisés+décédés).
I0, R0 = 1, 0

# Individus sains au départ
S0 = N - I0 - R0

# beta l'infectiosité et gamma le taux de rétablissement moyen (en 1/jours).
beta, gamma = 0.6, 1.0/7.0

# échelle de temps (ici en jours)
t = np.linspace(0, 90, 90)

# Les équations différentielles du modèle SIR.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# vecteur initial
y0 = S0, I0, R0

# Intégration des équations différentielles
ret = odeint(deriv, y0, t, args=(N, beta, gamma))

S, I, R = ret.T

#on calcule le total des décès sur la base du taux de mortalité
D = np.cumsum(I*0.005)

# Plot de la figure avec plotly
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
               name="sains"))
fig.add_trace(
    go.Scatter(x=t, y=I, marker=dict(color='#EF553B',size=1), marker_line=dict(width=1),
               name="infectés" ))
fig.add_trace(
    go.Scatter(x=t, y=R, marker=dict(color='#000000', size=1), marker_line=dict(width=1),
               name="removed"))

fig.update_xaxes(title_text="jours")
fig.update_yaxes(title_text="population")
fig.update_layout(title_text="Modèle SIR")
plot(fig)

