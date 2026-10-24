import os, re, struct, zlib
p = "android/app/src/main/AndroidManifest.xml"
m = open(p, encoding="utf8").read()
assert "<application" in m, "AndroidManifest inattendu"
m = m.replace("<application",
 '<uses-feature android:name="android.software.leanback" android:required="false"/>\n'
 '    <uses-feature android:name="android.hardware.touchscreen" android:required="false"/>\n'
 '    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM"/>\n'
 '    <application android:banner="@drawable/tv_banner"', 1)
m, n = re.subn(r'(<category android:name="android\.intent\.category\.LAUNCHER"\s*/>)',
 r'\1\n                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />', m, count=1)
assert n == 1, "categorie LAUNCHER introuvable"
open(p, "w", encoding="utf8").write(m)

def png(w, h, rgb):
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    def ch(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))
d = "android/app/src/main/res/drawable"
os.makedirs(d, exist_ok=True)
open(d + "/tv_banner.png", "wb").write(png(320, 180, (14, 23, 48)))
print("Manifest et banniere TV OK")
