
"""importation"""

from plotly.offline import plot  # pour travailler en offline!
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint


# Population totale, N.
N = 10000
# Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
I0, D0, R0 = 1, 0, 0
# Tous les autres sont susceptibles d'être touchés.
S0 = N - I0 - R0 - D0
# beta le taux de contact, mu guérison et théta mort
beta, mu, theta = 0.6, 0.28, 0.13
# la grille de temps pour le graphique (en jours)
t = np.linspace(0, 90, 90)

def deriv(y, t, N, beta, mu, theta):
    S, I, D, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - (mu+theta) * I
    dDdt = theta * I
    dRdt = mu * I
    return dSdt, dIdt, dDdt, dRdt

# vecteur initial
y0 = S0, I0, D0, R0
# Lance l'intégration des équations différentielles
ret = odeint(deriv, y0, t, args=(N, beta,mu, theta))

S, I, D, R = ret.T

# Trace les courbes
fig = go.Figure()
fig.update_layout(title_text="Modèle SIDR")

fig.add_trace(
    go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
               name="sains"))
fig.add_trace(
    go.Scatter(x=t, y=I, marker=dict(color='#EF553B',size=1), marker_line=dict(width=1),
               name="infectés" ))
fig.add_trace(
    go.Scatter(x=t, y=D, marker=dict(color='#AB63FA', size=1), marker_line=dict(width=1),
               name="Décès"))
fig.add_trace(
    go.Scatter(x=t, y=R, marker=dict(color='#00CC96', size=1), marker_line=dict(width=1),
               name="guéris"))

fig.update_xaxes(title_text="jours")
plot(fig)
