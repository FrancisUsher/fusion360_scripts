import adsk.core


def cross(u, v):
    # Compute cross-product of two vectors
    return adsk.core.Vector3D.create(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x
    )


def split(u, v, points):
    # return points on left side of UV
    return [p for p in points if cross_mag(p, u, v) < 0]


def cross_mag(p, u, v):
    ui = adsk.core.Application.get().userInterface
    uc = adsk.core.Vector3D.create(u.x, u.y, u.z)
    pc = adsk.core.Vector3D.create(p.x, p.y, p.z)
    vc = adsk.core.Vector3D.create(v.x, v.y, v.z)
    try:
        pc.subtract(uc)
        vc.subtract(uc)
    except TypeError as err:
        ui.messageBox('pc:{}\nu:{}'.format(pc, uc))
        raise TypeError
    except AttributeError as err:
        ui.messageBox('pc:{}\nu:{}'.format(pc, uc))
        raise AttributeError
    return cross(pc, vc).z


def extend(u, v, points):
    if not points:
        return []

    # find furthest point W, and split search to WV, UW
    w = min(points, key=lambda p: cross_mag(p, u, v))
    p1, p2 = split(w, v, points), split(u, w, points)
    return extend(w.asVector(), v, p1) + [w] + extend(u, w.asVector(), p2)


def convex_hull(points):
    # find two hull points, U, V, and split to left and right search
    u = min(points, key=lambda p: p.x).asVector()
    v = max(points, key=lambda p: p.x).asVector()
    left, right = split(u, v, points), split(v, u, points)

    # find convex hull on each side
    return [v] + extend(u, v, left) + [u] + extend(v, u, right) + [v]
