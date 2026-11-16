# Mixkit per-asset license audit (2026-11-16, read-only, no mutations)
Mixkit has two licenses. Asset page marker data-license="videoFree" = Stock Video Free License. "videoRestricted" = Mixkit Restricted License (personal use only, not for monetized/commercial publishing). Checked live on each asset page (id redirect https://mixkit.co/free-stock-video/x-<id>/).
Source of used ids: "mixkit-<id>" in the GitHub Actions logs of each generate run (the ids downloaded for that run; the log does not prove every downloaded clip made the final cut). YouTube status from the upload step's PRIVACY value and an unauthenticated oEmbed probe (200 = viewable, 403 = not public).

| Run | Upload | Mixkit ids -> license |
|---|---|---|
| 43727729767 | https://youtu.be/NZZY99Wh8dM PUBLIC (oEmbed 200, "Why birds fly away when firecrackers burst #Shorts") | 2560 Free; 19179, 17978, 15209, 11007 RESTRICTED |
| 43725042592 | https://youtu.be/dQiGs9m8HcA PUBLIC (oEmbed 200, same title) | no Mixkit ids in log; archive.org NPS items only (license not audited here) |
| 43718316894 | https://youtu.be/B9QsfBgkF4Y private at upload (oEmbed 403) | 9949, 49058, 26381 RESTRICTED; 22732, 1779 Free |
| 43709294618 | no upload in log (artifact only) | 9774, 45376, 44973, 44868, 25354 all RESTRICTED |
| 43704307326 (first cats video, Aria voice) | no upload in log (artifact only) | 9949, 49058, 26381 RESTRICTED; 22732, 1779 Free |
Private uploads (B9QsfBgkF4Y, qNJUkmW09ok, yLjseqCVB14, toSDEHipg0Y) are NOT public per oEmbed 403; qNJUkmW09ok, yLjseqCVB14, toSDEHipg0Y are archive.org-only. Current visibility could have changed after upload; not checked via authenticated API (token has upload scope only).
Gate: scripts/scrape_materials.py now fetches each candidate's asset page and accepts only data-license="videoFree"; errors, 429s, or missing markers reject (fail closed).
No takedown, edit or deletion done; none authorized.
