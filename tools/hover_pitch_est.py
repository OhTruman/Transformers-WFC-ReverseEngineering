"""Pitch-plane estimate of the original WFC hover car crossing a step riser.
Model (from script): 4 probes on diagonals at COM + R*(+-1,+-1)/sqrt2, probing along body -Z, TnSpring implicit law
per probe (m_i = M/4), force applied along body +Z scaled by (-dir . N) (flat ground N=(0,0,1)), never negative.
Grounded: no pitch correction (UpdateTurn yaw-only), RB angular/linear damping 0. Body gravity gb; spring gravity gs.
Script tick dt_s; physics integrates the tick's forces over n substeps (semi-implicit Euler)."""
import math


def run(M, Iy, R, K, B, rest, riser, speed=1500.0, gb=-1940.4, gs=-2940.0, dt=1/30., sub=2, T=3.0):
    m = M / 4.0
    xo = R / math.sqrt(2)                   # fore/aft lever arm of each probe pair
    def ground(x): return riser if x > 0.0 else 0.0
    # state: COM x (moves at constant speed), z, vz, pitch th (nose up +), w
    x = -300.0
    z = 150.0; vz = 0.0; th = 0.0; w = 0.0
    prevL = [-1.0, -1.0]                     # front, back spring lengths (TnSpring _Length; -1 = reset)
    maxth = 0.0; minth = 0.0
    t = 0.0
    # settle first on flat ground
    hist = []
    while t < T:
        # --- script tick: springs
        Fs = []
        for i, sgn in enumerate((+1, -1)):   # front (+x), back (-x)
            px = x + sgn * xo * math.cos(th)
            pz = z + sgn * xo * math.sin(th)
            dz = -math.cos(th)                # probe dir z component (body -Z)
            L = (pz - ground(px)) / max(1e-6, math.cos(th))   # distance along probe to ground plane
            if L > rest:                      # no contact
                prevL[i] = -1.0 if prevL[i] < 0 else rest
                Fs.append(0.0); continue
            L = max(0.0, L)
            v = (L - prevL[i]) / dt if prevL[i] >= 0 else 0.0
            prevL[i] = L
            g = -dz * gs
            Kp, Bp = K / m, B / m
            vp = (v + dt * (Kp * (rest - L) + g)) / (1 + Bp * dt + Kp * dt * dt)
            F = m * ((vp - v) / dt - g)
            F = max(0.0, math.cos(th) * F)    # (-dir . N) * F, never pulls
            Fs.append(2 * F)                  # two probes per side
        # --- physics substeps with the tick's forces held constant
        h = dt / sub
        for _ in range(sub):
            Fz = (Fs[0] + Fs[1]) * math.cos(th)
            tau = (Fs[1] - Fs[0]) * xo        # front force pitches nose up: sign so nose-up = +th
            tau = -tau
            vz += (Fz / M + gb) * h
            w += (tau / Iy) * h
            z += vz * h; th += w * h
        x += speed * dt; t += dt
        if x > 0: maxth = max(maxth, th); minth = min(minth, th)
        hist.append((t, x, z, math.degrees(th)))
    return math.degrees(maxth), math.degrees(minth), hist


if __name__ == '__main__':
    for name, M, Iy, R, K, B, rest in (('Car (HoverCar_Physics)', 1500, 9.8e6, 100, 8000, 4000, 200),
                                       ('Truck (HoverTruck_Physics, K=CDO 10000)', 2500, 4.64e7, 185, 10000, 4000, 250)):
        for riser in (12.5, 25.0):
            for gs in (-2940.0, -1940.4):
                mx, mn, h = run(M, Iy, R, K, B, rest, riser, gs=gs)
                print('%-42s riser %5.1f UU  gs %7.1f : pitch max %+6.2f deg  min %+6.2f deg' % (name, riser, gs, mx, mn))
