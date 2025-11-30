# 📡 GPS Basics --- Super Simple Revision Notes

## ⭐ What is GPS?

GPS is a **receiver**.\
It does NOT send signals.\
It only **listens to signals from satellites**.

Just like an FM radio:\
The station sends the signal → The radio only listens.\
Satellites send the signal → The GPS module only listens.

------------------------------------------------------------------------

## 🛰️ What do satellites send?

Each GPS satellite repeatedly sends:

1.  **Exact time** (from an atomic clock)\
2.  **Its own position** in orbit

The GPS receiver picks up those signals and uses math to calculate your
location.

------------------------------------------------------------------------

## 🧮 How does GPS find your position?

Imagine you ask your friends:

-   "How far are you from me?"\
-   Then you draw a circle around each friend using the distance.

**1 friend →** You could be anywhere on the circle\
**2 friends →** Two possible points\
**3 friends →** The circles meet at **one exact point**

GPS does the same thing.

------------------------------------------------------------------------

## 🌍 Why do we need 3 satellites on Earth?

On Earth, GPS works mostly in 2D (plus slight elevation).\
So **3 satellites** are enough to find your location.

Three distance circles intersect → your position.

------------------------------------------------------------------------

## 🚀 Why do we need 4 satellites in space?

In space, it's a full 3D environment (x, y, z axes).\
To get position + height accurately, GPS needs **4 satellites**.

------------------------------------------------------------------------

## ⏱️ The Time Problem (Very Important!)

Satellites use **super-accurate atomic clocks**.\
GPS modules use **simple crystal clocks** (less accurate).

This time difference creates **errors** in distance calculation.

That's why GPS receivers use an **extra satellite** to fix and correct
the timing error.

------------------------------------------------------------------------

## 🧠 A Very Simple Real-Life Example

You call 3 friends and ask:

-   Friend 1: "I'm 4 km away from you."\
-   Friend 2: "I'm 3 km away."\
-   Friend 3: "I'm 5 km away."

If all their clocks are correct → You can find your exact spot.\
If one clock is wrong → All distances become wrong → Wrong location.

GPS works exactly like this.

------------------------------------------------------------------------

## 📦 Final Summary (For Quick Revision)

-   GPS = **receiver**, listens only\
-   Satellites send **time + position**\
-   GPS calculates distance from satellites\
-   **3 satellites** → position on Earth\
-   **4 satellites** → position in space\
-   Time mismatch (atomic vs crystal clocks) → error\
-   Extra satellite helps fix timing errors