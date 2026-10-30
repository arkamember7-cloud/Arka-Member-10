#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arka — یک‌فایلی: PostgreSQL + UI"""
from __future__ import annotations
import json, threading, time, uuid, secrets, sys, hashlib, os, base64, hmac, re, ssl, math, subprocess, tempfile, shutil, gzip, zlib
import urllib.request
import urllib.parse
import http.cookies
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

HOST, PORT = os.environ.get("ARKA_HOST", "127.0.0.1"), int(os.environ.get("PORT", "8000"))

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl" data-mode="auto">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#6B4EE6" id="tcMeta">
<title>آرکا | ARKA</title>
<link rel="icon" href="/logo.jpg">
<link rel="apple-touch-icon" href="/logo.jpg">
<link rel="stylesheet" href="/fonts.css">
<style>
:root{
  --bg:#F1EEFD;--surface:#fff;--surface2:#F5F2FF;--ink:#17133A;--muted:#7A759F;--line:#E4E0F7;
  --brand:#6B4EE6;--brand2:#4B2FD0;--coin:#F6A823;--coin-soft:#FFF2D6;--ok:#0E9F78;--bad:#E5476F;--warn:#B87400;
  --au1:var(--brand);--au2:var(--brand2);
  --shadow:0 10px 24px -18px rgba(60,35,170,.65);--lift:0 20px 38px -18px rgba(60,35,170,.55);
  color-scheme:light;
}
:root[data-mode="dark"]{
  --bg:#0E0B22;--surface:#17133A;--surface2:#1F1A4A;--ink:#EFEBFF;--muted:#A29CCB;--line:#2B2560;
  --coin-soft:#3B2D0E;--ok:#35E0B0;--bad:#FF7B9B;--warn:#F6C25B;--au1:color-mix(in srgb,var(--brand) 45%,#0E0B22);--au2:color-mix(in srgb,var(--brand2) 25%,#0E0B22);--shadow:0 10px 24px -18px #000;--lift:0 20px 38px -18px #000;color-scheme:dark;
}
@media (prefers-color-scheme:dark){
  :root[data-mode="auto"]{
    --bg:#0E0B22;--surface:#17133A;--surface2:#1F1A4A;--ink:#EFEBFF;--muted:#A29CCB;--line:#2B2560;
    --coin-soft:#3B2D0E;--ok:#35E0B0;--bad:#FF7B9B;--warn:#F6C25B;--au1:color-mix(in srgb,var(--brand) 45%,#0E0B22);--au2:color-mix(in srgb,var(--brand2) 25%,#0E0B22);--shadow:0 10px 24px -18px #000;--lift:0 20px 38px -18px #000;color-scheme:dark;
  }
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{font-family:Vazirmatn,'Noto Naskh Arabic','Noto Sans Arabic',Tahoma,system-ui,sans-serif;background:var(--bg);color:var(--ink);display:flex;justify-content:center;line-height:1.7}
button,input{font:inherit;color:inherit}
button{background:none;border:0;cursor:pointer}
svg{display:block}
a{color:inherit}
:focus-visible{outline:3px solid var(--coin);outline-offset:2px;border-radius:12px}
.app{width:100%;max-width:430px;min-height:100vh;padding-bottom:124px;position:relative;overflow-x:hidden;margin:0 auto;background:var(--bg)}
.view{display:none}.view.on{display:block;animation:vin .35s ease-out}
.clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere}

/* ===== header ===== */
.top{position:relative;width:100%;box-sizing:border-box;color:#fff;border-radius:0 0 40px 40px;overflow:hidden;--tc:var(--brand);--tc2:var(--brand2);
  background:radial-gradient(circle at 12% 0%,rgba(255,255,255,.22) 0 90px,transparent 91px),
  radial-gradient(circle at 105% 70%,rgba(255,255,255,.12) 0 110px,transparent 111px),
  radial-gradient(rgba(255,255,255,.1) 1.5px,transparent 1.6px) 0 0/18px 18px,
  linear-gradient(165deg,var(--tc) 0%,var(--tc2) 100%);
  padding:calc(env(safe-area-inset-top) + 30px) 20px 100px;transition:background .3s}
.top.pgh{padding-bottom:96px}
.row{display:flex;align-items:center;gap:10px}
.row>*{min-width:0}
.avatar{width:52px;height:52px;border-radius:50%;flex:none;overflow:hidden;border:3px solid rgba(255,255,255,.6);background:#fff}
.avimg{width:100%;height:100%;object-fit:cover;display:block;border-radius:50%}
.who{flex:1;min-width:0}.who small{display:block;font-size:12px;opacity:.85;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.who b{display:block;font-size:18px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ib{width:44px;height:44px;border-radius:15px;background:rgba(255,255,255,.18);display:grid;place-items:center;position:relative;flex:none;color:#fff}
.ib svg.pop{animation:pop .45s cubic-bezier(.3,1.6,.5,1)}
@keyframes pop{from{transform:rotate(-80deg) scale(.4);opacity:0}to{transform:none;opacity:1}}
.ib i.bellDot{position:absolute;top:8px;left:10px;width:12px;height:12px;border-radius:50%;background:var(--coin);border:2px solid var(--tc2);display:none;font-size:0;line-height:0}
.ib i.bellDot.on{display:block}
.pgtitle{font-size:26px;font-weight:900;line-height:1.3;overflow-wrap:anywhere}
.pgsub{font-size:13px;opacity:.85;margin-top:2px;overflow-wrap:anywhere}
.balpill{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.18);border-radius:99px;padding:5px 12px 5px 6px;font-weight:800;font-size:14px;white-space:nowrap;flex:none}
.balpill svg{width:26px;height:26px}.balpill small{font-weight:500;opacity:.85;font-size:11px}

/* ===== balance card ===== */
.balance{margin:-70px 20px 0;border-radius:28px;padding:18px;position:relative;overflow:hidden;display:flex;align-items:center;gap:14px;
  background:linear-gradient(135deg,var(--surface) 55%,var(--surface2) 100%);box-shadow:var(--lift);border:1px solid var(--line)}
.balance::before{content:"";position:absolute;left:-44px;top:50%;width:160px;height:160px;transform:translateY(-50%);border-radius:50%;border:14px solid rgba(246,168,35,.11)}
.balance::after{content:"";position:absolute;left:-4px;top:50%;width:80px;height:80px;transform:translateY(-50%);border-radius:50%;border:3px dashed rgba(246,168,35,.28)}
.coinw{position:relative;flex:none;width:68px;height:68px}
.coinw svg{width:68px;height:68px;filter:drop-shadow(0 6px 8px rgba(198,120,0,.35))}
.balance .m{position:relative;z-index:1;flex:1;min-width:0}
.balance small{display:block;color:var(--muted);font-size:13px}
.balance strong{font-size:32px;font-weight:900;line-height:1.2;letter-spacing:-.5px}
.unit{font-size:12px;font-weight:800;color:var(--warn);background:var(--coin-soft);padding:2px 10px;border-radius:99px;margin-inline-start:6px;vertical-align:middle}
.mini{position:relative;z-index:1;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-radius:14px;padding:9px 14px;font-weight:800;font-size:13px;flex:none}

h2.sec{font-size:17px;font-weight:900;margin:24px 20px 12px}

/* ===== member card ===== */
.mc{margin:16px 20px 0;perspective:900px;height:192px;touch-action:pan-y;cursor:pointer}
.mc-t{position:relative;width:100%;height:100%;transition:transform .65s cubic-bezier(.4,.1,.2,1);transform-style:preserve-3d}
.mc.flipped .mc-t{transform:rotateY(180deg)!important}
.mc-face,.mc-back{position:absolute;inset:0;border-radius:28px;overflow:hidden;color:#fff;padding:18px 20px;display:flex;flex-direction:column;justify-content:space-between;-webkit-backface-visibility:hidden;backface-visibility:hidden}
.mc-back{transform:rotateY(180deg);
  background:radial-gradient(circle at 8% -10%,color-mix(in srgb,var(--brand) 70%,transparent) 0 120px,transparent 121px),radial-gradient(circle at 100% 110%,rgba(246,168,35,.32) 0 100px,transparent 101px),linear-gradient(145deg,#1a1448 0%,#0F0B33 100%);
  box-shadow:0 26px 36px -22px rgba(20,10,80,.9),inset 0 0 0 1px rgba(255,255,255,.1)}
.mc-back .bal-lab{font-size:11px;opacity:.65;letter-spacing:1px}
.mc-back .bal-val{font-size:28px;font-weight:900;margin-top:4px;letter-spacing:-.5px}
.mc-back .bal-val span{font-size:13px;font-weight:700;opacity:.7;margin-inline-start:6px}
.mc-back .hint{font-size:11px;opacity:.45;margin-top:auto}
.mc-face{
  background:radial-gradient(circle at 92% -8%,color-mix(in srgb,var(--brand) 80%,transparent) 0 130px,transparent 131px),radial-gradient(circle at 0% 112%,rgba(246,168,35,.38) 0 112px,transparent 113px),radial-gradient(rgba(255,255,255,.07) 1.2px,transparent 1.3px) 0 0/14px 14px,linear-gradient(135deg,color-mix(in srgb,var(--brand2) 75%,#000) 0%,#0F0B33 100%);
  box-shadow:0 26px 36px -22px rgba(20,10,80,.9),inset 0 0 0 1px rgba(255,255,255,.1)}
.mc-face::after{content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.2) 44%,rgba(110,200,255,.2) 50%,rgba(255,170,255,.18) 56%,transparent 70%);background-size:260% 100%;background-position:var(--sx,120%) 0;animation:sheen 2.6s .7s 1 both}
@keyframes sheen{from{background-position:120% 0}to{background-position:-20% 0}}
.mc-wm{position:absolute;inset-inline-end:-26px;bottom:-46px;opacity:.1;pointer-events:none}
.mc-r1{display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1}
.mc-brand{display:flex;align-items:center;gap:8px;font-weight:900;letter-spacing:6px;font-size:14px}
.mc-chip{position:relative;z-index:1;filter:drop-shadow(0 3px 5px rgba(0,0,0,.35))}
.mc-r3{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;position:relative;z-index:1}
.mc-n{min-width:0;flex:1}.mc-n small,.mc-d small{display:block;font-size:10.5px;opacity:.65}
.mc-n b{display:block;font-size:19px;font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.5}
.mc-d{text-align:end;flex:none}.mc-d b{display:block;font-size:14px;font-weight:800;line-height:1.7;white-space:nowrap}

/* ===== app tiles ===== */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 20px}
.tile{position:relative;overflow:hidden;background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:26px 12px 22px;display:flex;flex-direction:column;align-items:center;gap:12px;box-shadow:var(--shadow);transition:transform .18s}
.tile::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,color-mix(in srgb,var(--tc) 26%,transparent),transparent 66%);pointer-events:none}
.tile::after{content:"";position:absolute;inset-inline:32%;bottom:0;height:4px;border-radius:4px 4px 0 0;background:var(--tc)}
.tile h3{font-size:17px;font-weight:900;position:relative}
.tile:active{transform:scale(.97)}
.logo{display:block;flex:none;filter:drop-shadow(0 8px 10px color-mix(in srgb,var(--tc,#6B4EE6) 50%,transparent));position:relative;z-index:1}
.logo-img{display:block;flex:none;object-fit:cover;border-radius:28%;position:relative;z-index:1}

/* ===== list rows ===== */
.list{margin:0 20px;background:var(--surface);border:1px solid var(--line);border-radius:26px;overflow:hidden;box-shadow:var(--shadow)}
.lr{display:flex;align-items:center;gap:14px;width:100%;padding:14px 16px;text-align:start}
.lr+.lr{border-top:1px solid var(--line)}
.ico{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;flex:none;background:color-mix(in srgb,var(--tc) 14%,var(--surface));color:var(--tc)}
.lr .t{flex:1;min-width:0}.lr b{display:block;font-size:15px;font-weight:800}.lr span.s{font-size:12px;color:var(--muted)}
.lr .ch{color:var(--muted)}
.lr:active{background:var(--bg)}
.badge{background:var(--bad);color:#fff;font-size:11px;font-weight:800;border-radius:99px;padding:0 8px}

/* ===== page header ===== */
.ph{display:flex;align-items:center;gap:12px}
.ph .tt{flex:1;min-width:0}
.ph .tt b{display:block;font-size:24px;font-weight:900;line-height:1.35;white-space:nowrap}
.ph .tt small{display:block;font-size:13px;opacity:.85;line-height:1.6}
.ph .big{width:54px;height:54px;border-radius:19px;background:rgba(255,255,255,.18);display:grid;place-items:center;flex:none;color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)}

/* ===== platform page ===== */
.cats{display:grid;gap:14px;margin:-58px 16px 0;position:relative}
.cat{background:var(--surface);border:1px solid var(--line);border-radius:30px;box-shadow:var(--lift);overflow:hidden}
.cat-h{display:flex;align-items:center;gap:14px;width:100%;padding:16px;text-align:start}
.cat-ic{width:54px;height:54px;border-radius:19px;display:grid;place-items:center;flex:none;color:#fff;background:linear-gradient(135deg,var(--tc),var(--tc2));box-shadow:0 14px 22px -12px var(--tc)}
.cat-t{flex:1;min-width:0}.cat-t b{display:block;font-size:17px;font-weight:900;line-height:1.6}.cat-t small{color:var(--muted);font-size:12.5px}
.cat-ch{width:36px;height:36px;border-radius:13px;background:var(--surface2);display:grid;place-items:center;color:var(--tc);transition:transform .35s,background .25s;flex:none}
.cat.open .cat-ch{transform:rotate(-90deg);background:var(--tc);color:#fff}
.cat-b{display:grid;grid-template-rows:0fr;transition:grid-template-rows .4s cubic-bezier(.2,.8,.2,1)}
.cat.open .cat-b{grid-template-rows:1fr}
.cat-bi{overflow:hidden;min-height:0}
.cat-list{display:grid;gap:12px;padding:2px 12px 14px}
.pc{display:block;width:100%;text-align:start;background:var(--surface2);border:1px solid var(--line);border-radius:22px;padding:14px;position:relative;overflow:hidden;transition:transform .15s}
.pc::before{content:"";position:absolute;inset-block:14px;inset-inline-start:0;width:4px;border-radius:0 4px 4px 0;background:var(--tc)}
.pc:active{transform:scale(.985)}
.pc-h{display:flex;gap:10px;align-items:flex-start}
.pc-h b{flex:1;min-width:0;font-size:14.5px;font-weight:800;line-height:1.8;overflow-wrap:anywhere}
.pc-go{width:30px;height:30px;border-radius:50%;background:var(--tc);color:#fff;display:grid;place-items:center;flex:none;box-shadow:0 8px 14px -8px var(--tc)}
.pc-s{display:grid;grid-template-columns:1fr 1fr 1.35fr;margin-top:12px;background:var(--surface);border-radius:16px;padding:10px 2px}
.pc-s div{text-align:center;padding:0 4px;min-width:0}
.pc-s div+div{border-inline-start:1px dashed var(--line)}
.pc-s small{display:block;font-size:10.5px;color:var(--muted);line-height:1.6}
.pc-s b{display:block;font-size:14.5px;font-weight:900;line-height:1.5}
.pc-s .pr b{color:var(--tc)}
.nop{margin:-58px 20px 0;position:relative;background:var(--surface);border:2px dashed var(--line);border-radius:30px;padding:36px 18px;text-align:center;box-shadow:var(--shadow)}
.nop .logo,.nop .logo-img{margin:0 auto 14px;opacity:.55;filter:grayscale(.7)}
.nop h3{font-size:18px;font-weight:900}.nop p{font-size:13px;color:var(--muted);margin-top:4px}

/* ===== order sheet ===== */
.lbl{font-size:12.5px;font-weight:800;color:var(--muted);margin:16px 0 7px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.lbl em{font-style:normal;font-weight:600;font-size:11.5px}
.inp{width:100%;height:54px;border-radius:18px;border:2px solid var(--line);background:var(--surface2);padding:0 16px;font-size:15px;outline:0;transition:border-color .2s}
.inp:focus{border-color:var(--tc,var(--brand))}
.ltr{direction:ltr;text-align:left}
.info{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:4px 16px;margin-top:10px}
.info div{display:flex;justify-content:space-between;gap:14px;padding:9px 0;font-size:13px}
.info div+div{border-top:1px dashed var(--line)}
.info span{color:var(--muted);flex:none}.info b{font-weight:800;text-align:end;overflow-wrap:anywhere}
.smp{margin-top:12px;font-size:12px;color:var(--muted)}
.smp code{display:block;direction:ltr;text-align:left;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--ink);background:var(--surface2);border-radius:10px;padding:5px 10px;margin-top:6px;overflow-wrap:anywhere}
.notes{margin-top:12px;display:grid;gap:6px}
.notes p{font-size:12px;line-height:1.8;color:var(--muted);background:var(--coin-soft);border-radius:14px;padding:8px 12px}
.sum{background:var(--surface2);border-radius:20px;padding:12px 16px;margin-top:16px;font-size:13px}
.sum div{display:flex;justify-content:space-between;padding:2px 0;color:var(--muted)}
.sum .t{color:var(--ink);font-weight:900;font-size:18px;border-top:1px dashed var(--line);margin-top:6px;padding-top:8px}
.sum .t b{color:var(--tc,var(--brand))}
.err{min-height:22px;margin:8px 0;font-size:12.5px;font-weight:800;color:var(--bad)}
.err a{color:var(--brand);text-decoration:underline}
.btn{height:58px;border-radius:20px;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:900;font-size:16px;transition:transform .1s}
.btn:active{transform:scale(.98)}
.btn.brand{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;box-shadow:0 12px 20px -12px var(--brand)}
.btn.soft{background:var(--surface2);border:2px solid var(--line);color:var(--ink)}
.btn.full{width:100%}
.btn[disabled]{opacity:.45;pointer-events:none}

/* ===== product sheet ===== */
.sheet.ps{display:flex;flex-direction:column;overflow:hidden;padding-bottom:0}
.ps-scroll{flex:1;min-height:0;overflow-y:auto;padding-bottom:12px;overscroll-behavior:contain}
.ps-hero{border-radius:26px;padding:16px;color:#fff;display:flex;gap:14px;align-items:center;position:relative;overflow:hidden;
  background:radial-gradient(circle at 10% 0%,rgba(255,255,255,.25) 0 70px,transparent 71px),radial-gradient(rgba(255,255,255,.12) 1.5px,transparent 1.6px) 0 0/16px 16px,linear-gradient(150deg,var(--tc),var(--tc2))}
.ps-hero h3{font-size:16px;font-weight:900;line-height:1.8;min-width:0;overflow-wrap:anywhere;position:relative}
.ps-st{display:grid;grid-template-columns:1fr 1fr 1.35fr;gap:8px;margin-top:10px}
.ps-st div{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:10px 4px;text-align:center}
.ps-st small{display:block;font-size:10.5px;color:var(--muted);line-height:1.6}.ps-st b{display:block;font-size:15px;font-weight:900}
.ps-st .pr b{color:var(--tc)}
.sec2{font-size:13.5px;font-weight:900;margin:20px 2px 10px;display:flex;align-items:center;gap:8px;color:var(--ink)}
.sec2 svg{color:var(--tc)}
.specs{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sp{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:10px 12px;display:flex;gap:10px;align-items:flex-start;min-width:0}
.sp.w{grid-column:1/-1}
.sp .i{width:34px;height:34px;border-radius:12px;display:grid;place-items:center;flex:none;background:color-mix(in srgb,var(--tc) 14%,var(--surface));color:var(--tc)}
.sp small{display:block;font-size:11px;color:var(--muted);line-height:1.6}.sp b{display:block;font-size:13px;font-weight:800;line-height:1.7;overflow-wrap:anywhere}
.nt{background:var(--coin-soft);border-radius:20px;margin-top:12px;overflow:hidden}
.nt-h{display:flex;align-items:center;gap:10px;width:100%;padding:12px 14px;font-weight:800;font-size:13px;color:var(--warn)}
.nt-h>svg:last-child{transition:transform .3s}.nt.open .nt-h>svg:last-child{transform:rotate(-90deg)}
.nt-b{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s}
.nt.open .nt-b{grid-template-rows:1fr}
.nt-bi{overflow:hidden;min-height:0}
.nt-bi p{font-size:12px;line-height:1.9;color:var(--ink);padding:0 14px 8px}
.sheet.ps .fi .inp{--tc:inherit}
.smp2{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px;font-size:11.5px;color:var(--muted)}
.smp2 button{direction:ltr;font-family:ui-monospace,Menlo,monospace;font-size:12px;background:var(--surface);border:1px dashed var(--tc);color:var(--ink);border-radius:12px;padding:5px 10px;overflow-wrap:anywhere;text-align:left}
.buybar{flex:none;padding:10px 0 calc(14px + env(safe-area-inset-bottom));border-top:1px solid var(--line);background:var(--bg)}
.buybar .err{min-height:18px;margin:2px 2px 6px}
.bb{display:flex;align-items:center;gap:12px}
.bb .tot{flex:none}.bb .tot small{display:block;font-size:11.5px;color:var(--muted);line-height:1.4}
.bb .tot b{font-size:22px;font-weight:900;color:var(--tc)}.bb .tot span{font-size:12px;color:var(--muted)}
.bb .btn{flex:1;height:54px;font-size:15px}

/* ===== orders ===== */
.ostat{margin:-62px 16px 0;position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:30px;padding:8px;box-shadow:var(--lift)}
.ostat button{padding:12px 4px 10px;border-radius:23px;text-align:center;color:var(--muted);transition:background .25s,color .25s}
.ostat b{display:block;font-size:23px;font-weight:900;color:var(--ink);line-height:1.4}
.ostat span{font-size:12px;font-weight:700}
.ostat button[aria-pressed="true"]{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;box-shadow:0 12px 18px -10px var(--brand)}
.ostat button[aria-pressed="true"] b{color:#fff}
.ord{margin:14px 16px 0;background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:16px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.ord::before{content:"";position:absolute;inset-inline-start:0;top:20px;bottom:20px;width:4px;border-radius:0 4px 4px 0;background:var(--tc)}
.ord-h{display:flex;gap:12px;align-items:center}
.ord-t{flex:1;min-width:0}.ord-t b{display:block;font-size:14.5px;line-height:1.7;font-weight:800}.ord-t small{display:block;color:var(--muted);font-size:11.5px;margin-top:2px;overflow-wrap:anywhere}
.ring{position:relative;width:52px;height:52px;flex:none}
.ring svg{transform:rotate(-90deg);display:block}
.ring .bg{stroke:var(--surface2)}.ring .fg{stroke:var(--tc);transition:stroke-dashoffset .6s}
.ring span{position:absolute;inset:0;display:grid;place-items:center;font-size:11.5px;font-weight:900}
.ord-lk{display:flex;align-items:center;gap:8px;direction:ltr;background:var(--surface2);border-radius:14px;padding:8px 12px;margin-top:12px;font-size:12px;color:var(--muted)}
.ord-lk svg{flex:none}.ord-lk span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;text-align:left}
.ord-f{display:flex;align-items:center;gap:8px;margin-top:12px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;border-radius:99px;padding:2px 11px;font-size:12px;font-weight:800;background:var(--surface2);white-space:nowrap}
.pill.st-done{color:var(--ok);background:color-mix(in srgb,var(--ok) 14%,var(--surface))}
.pill.st-run{color:var(--tc);background:color-mix(in srgb,var(--tc) 14%,var(--surface))}
.pill.st-q{color:var(--warn);background:var(--coin-soft)}
.ord-pr{margin-inline-start:auto;font-weight:900;font-size:15px;white-space:nowrap}.ord-pr small{font-weight:500;font-size:11px;color:var(--muted)}
.oa{display:flex;gap:8px;margin-top:12px}
.oa button{flex:1;height:44px;border-radius:15px;background:var(--surface2);font-size:12.5px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:6px}
.oa button:active{background:var(--line)}
.empty{margin:16px 20px 0;text-align:center;color:var(--muted);padding:38px 14px;background:var(--surface);border:2px dashed var(--line);border-radius:28px;font-size:14px;overflow-wrap:anywhere;line-height:1.9}
.empty svg{margin:0 auto 10px;opacity:.45}

/* ===== wallet ===== */
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 20px}
.chip{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:14px 4px;font-weight:900;font-size:14px;position:relative;box-shadow:var(--shadow)}
.chip small{display:block;font-weight:500;color:var(--muted);font-size:11px}
.tx{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 16px;font-size:13.5px;font-weight:700}
.tx>div{min-width:0;overflow-wrap:anywhere}
.tx+.tx{border-top:1px solid var(--line)}
.tx small{display:block;color:var(--muted);font-weight:500;font-size:11px}
.plus{color:var(--ok);font-weight:900;flex:none}.minus{color:var(--bad);font-weight:900;flex:none}
.tx.none{justify-content:center;color:var(--muted);font-weight:500;padding:22px 16px}

/* ===== me ===== */
.prof{margin:-64px 20px 0;background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:18px;box-shadow:var(--lift);position:relative}
.prof .a{display:flex;gap:14px;align-items:center}
.prof .av{width:66px;height:66px;border-radius:50%;flex:none;position:relative;border:3px solid var(--line);padding:0}
.prof .av .cam{position:absolute;bottom:-4px;inset-inline-start:-4px;width:26px;height:26px;border-radius:50%;background:var(--brand);color:#fff;display:grid;place-items:center;border:2px solid var(--surface)}
.prof .nm{min-width:0;flex:1}
.prof b{font-size:18px;display:block;overflow-wrap:anywhere;line-height:1.5}.prof small{color:var(--muted);display:block;overflow-wrap:anywhere}
.card{margin:0 20px;background:var(--surface);border:1px solid var(--line);border-radius:26px;padding:16px;box-shadow:var(--shadow)}
.bars{display:grid;gap:12px}
.bar{display:grid;grid-template-columns:72px 1fr auto;gap:8px;align-items:center;font-size:12.5px;font-weight:700}
.bar i{display:block;height:11px;border-radius:9px;background:var(--surface2);overflow:hidden}
.bar i b{display:block;height:100%;border-radius:9px;background:var(--tc)}
.code{display:flex;justify-content:space-between;align-items:center;gap:8px;background:var(--surface2);border:2px dashed var(--brand);border-radius:18px;padding:8px 8px 8px 14px;font-weight:900;letter-spacing:3px;direction:ltr;font-size:18px}
.code .btn{padding:8px 16px;font-size:13px;letter-spacing:0;border-radius:13px;height:auto}
.cp{display:flex;gap:8px}.cp .inp{flex:1;height:48px}
.cp button{padding:0 18px;border-radius:16px;background:var(--brand);color:#fff;font-weight:800;font-size:13px}

/* ===== sheet ===== */
.sbg{position:fixed;inset:0;background:rgba(10,5,40,.6);backdrop-filter:blur(3px);z-index:50;display:none;align-items:flex-end}
.sbg.on{display:flex}
.sheet{background:var(--bg);width:100%;max-width:430px;margin:0 auto;max-height:90vh;overflow-y:auto;border-radius:30px 30px 0 0;padding:10px 18px calc(24px + env(safe-area-inset-bottom));animation:up .3s cubic-bezier(.2,.8,.2,1)}
.sheet::before{content:"";display:block;width:44px;height:5px;border-radius:9px;background:var(--line);margin:4px auto 16px}
@keyframes up{from{transform:translateY(50px);opacity:0}to{transform:none;opacity:1}}
.sh{font-size:18px;font-weight:900;margin-bottom:4px;overflow-wrap:anywhere;line-height:1.7}.shp{font-size:13px;color:var(--muted);margin-bottom:6px}
.chat{display:grid;gap:8px;max-height:44vh;overflow-y:auto;padding:4px 0}
.msg{max-width:84%;padding:9px 14px;border-radius:18px;font-size:13px;overflow-wrap:anywhere}
.msg.bot{background:var(--surface);border:1px solid var(--line);border-end-start-radius:4px}
.msg.me{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;margin-inline-start:auto;border-end-end-radius:4px}
.pre{display:flex;gap:6px;flex-wrap:wrap}
.pre button{background:var(--surface2);border:1px solid var(--line);border-radius:99px;padding:3px 13px;font-size:12.5px;font-weight:800}
.pf{display:grid;place-items:center;margin:6px 0 4px}
.pfb{position:relative;width:96px;height:96px;border-radius:50%;padding:0;border:3px dashed var(--brand)}
.pfb .avimg{border-radius:50%}
.pfb .cam{position:absolute;bottom:-2px;inset-inline-end:-2px;width:32px;height:32px;border-radius:50%;background:var(--brand);color:#fff;display:grid;place-items:center;border:3px solid var(--bg)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}

/* ===== nav ===== */
.nav{position:fixed;bottom:calc(env(safe-area-inset-bottom) + 12px);right:50%;transform:translateX(50%);width:calc(100% - 28px);max-width:402px;display:flex;gap:6px;padding:8px;background:var(--surface);border-radius:30px;box-shadow:0 18px 40px -14px rgba(60,35,170,.55),0 0 0 1px var(--line);z-index:10}
.nav button{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;height:58px;border-radius:22px;font-size:12px;font-weight:600;color:var(--muted);transition:background .25s,color .25s,flex .25s;position:relative}
.nav button.on{flex:1.35;background:linear-gradient(160deg,var(--brand),var(--brand2));color:#fff;font-weight:800;box-shadow:0 12px 20px -12px var(--brand)}
.nav .badge{position:absolute;top:2px;inset-inline-end:12px;font-size:10px;padding:0 6px}
.toast{position:fixed;bottom:112px;left:50%;transform:translate(-50%,16px);background:var(--ink);color:var(--bg);padding:11px 20px;border-radius:16px;font-size:13.5px;font-weight:800;opacity:0;pointer-events:none;transition:.25s;z-index:95;max-width:90vw;text-align:center}
.toast.on{opacity:1;transform:translate(-50%,0)}
#fx{position:fixed;inset:0;pointer-events:none;z-index:96}

/* ===== auth ===== */
#auth{position:fixed;inset:0;z-index:90;display:none;overflow-y:auto;color:#fff;
  background:radial-gradient(circle at 14% 6%,rgba(255,255,255,.2) 0 110px,transparent 111px),
  radial-gradient(circle at 104% 48%,rgba(255,255,255,.1) 0 150px,transparent 151px),
  radial-gradient(rgba(255,255,255,.1) 1.5px,transparent 1.6px) 0 0/18px 18px,
  linear-gradient(165deg,var(--au1),var(--au2))}
#auth.on{display:block}
.au{max-width:430px;margin:0 auto;padding:calc(env(safe-area-inset-top) + 16px) 20px 36px;position:relative;min-height:100%}
.au-top{display:flex;justify-content:flex-start}
.au-logo{text-align:center;margin:2px 0 18px;position:relative}
.au-logo b{display:block;font-size:40px;font-weight:900;line-height:1.2;margin-top:4px}
.au-logo small{letter-spacing:9px;opacity:.85;font-size:12px}
.fl{position:absolute;pointer-events:none;opacity:.9}
.fl.a{top:6px;inset-inline-end:6px;animation:flt 5s ease-in-out infinite}
.fl.b{top:78px;inset-inline-start:2px;animation:flt 6.5s -2s ease-in-out infinite}
@keyframes flt{50%{transform:translateY(-10px) rotate(8deg)}}
.au-card{background:var(--surface);color:var(--ink);border-radius:32px;padding:18px;box-shadow:0 30px 50px -24px rgba(10,5,50,.8);position:relative}
.seg2{position:relative;display:grid;grid-template-columns:1fr 1fr;background:var(--surface2);border-radius:20px;padding:5px}
.seg2 .ind{position:absolute;inset-block:5px;inset-inline-start:5px;width:calc(50% - 5px);border-radius:16px;background:linear-gradient(135deg,var(--brand),var(--brand2));box-shadow:0 10px 18px -10px var(--brand);transition:transform .35s cubic-bezier(.3,1.2,.4,1)}
.au[data-tab=in] .seg2 .ind{transform:translateX(-100%)}
.seg2 button{position:relative;z-index:1;padding:11px 4px;font-weight:800;font-size:14px;color:var(--muted);transition:color .25s}
.au[data-tab=up] .seg2 button[data-t=up],.au[data-tab=in] .seg2 button[data-t=in]{color:#fff}
.form{display:grid;gap:12px;margin-top:18px;animation:fin .35s ease-out}
@keyframes fin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.au[data-tab=up] .form.in,.au[data-tab=in] .form.up{display:none}
.fi{position:relative;display:block}
.fi .fic{position:absolute;inset-inline-start:14px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none}
.fi .inp{padding-inline-start:46px;--tc:var(--brand)}
.fi .eye{position:absolute;inset-inline-end:8px;top:50%;transform:translateY(-50%);width:38px;height:38px;border-radius:12px;display:grid;place-items:center;color:var(--muted)}
.fi .eye+*{}
.fi.pw .inp{padding-inline-end:48px}
.fi .inp:focus{box-shadow:0 0 0 4px color-mix(in srgb,var(--brand) 18%,transparent)}
.au-err{white-space:pre-line;min-height:20px;font-size:12.5px;font-weight:800;color:var(--bad);margin:-2px 2px}
.au-pf{display:flex;align-items:center;gap:14px;background:var(--surface2);border-radius:22px;padding:10px 12px}
.au-pf .pfb{width:68px;height:68px;flex:none}
.au-pf .pfb .cam{width:26px;height:26px;border-width:2px}
.au-pf p{font-size:13px;font-weight:800}.au-pf small{display:block;font-size:11.5px;color:var(--muted);font-weight:500}

/* ===== حرکت‌ها ===== */
@keyframes vin{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.stg>*{animation:vin .5s both}
.stg>*:nth-child(1){animation-delay:.04s}.stg>*:nth-child(2){animation-delay:.1s}.stg>*:nth-child(3){animation-delay:.16s}
.stg>*:nth-child(4){animation-delay:.22s}.stg>*:nth-child(5){animation-delay:.28s}.stg>*:nth-child(6){animation-delay:.34s}
@keyframes shake{20%,60%{transform:translateX(-7px)}40%,80%{transform:translateX(7px)}}
.au-card.shake{animation:shake .4s}
.au-hint{display:flex;gap:8px;align-items:flex-start;font-size:11.5px;line-height:1.8;color:var(--muted);background:var(--surface2);border-radius:14px;padding:8px 12px;margin-top:-4px}
.au-hint svg{flex:none;margin-top:4px;color:var(--brand)}
.meter{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin:-4px 2px 0}
.meter i{height:5px;border-radius:9px;background:var(--surface2);transition:background .25s}
.meter[data-s="1"] i:nth-child(-n+1){background:#E5476F}
.meter[data-s="2"] i:nth-child(-n+2){background:#F6A823}
.meter[data-s="3"] i:nth-child(-n+3){background:#7BC043}
.meter[data-s="4"] i{background:var(--ok)}
.pst{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}
.pst div{background:var(--surface2);border-radius:18px;padding:10px 4px;text-align:center}
.pst b{display:block;font-size:15px;font-weight:900;line-height:1.5;overflow-wrap:anywhere}.pst span{font-size:11px;color:var(--muted)}


.nlist{display:grid;gap:10px;margin-top:8px}
.nitem{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:14px;box-shadow:var(--shadow)}
.nicon{width:40px;height:40px;border-radius:14px;display:grid;place-items:center;flex:none;background:color-mix(in srgb,var(--brand) 14%,var(--surface));color:var(--brand)}
.nbody{min-width:0;flex:1}.nbody b{display:block;font-size:13.5px;font-weight:800;line-height:1.7;overflow-wrap:anywhere}
.nbody small{display:block;font-size:11.5px;color:var(--muted);margin-top:4px}
.nempty{text-align:center;padding:36px 16px 24px;background:var(--surface);border:1px dashed var(--line);border-radius:24px;margin-top:8px}
.nempty-ic{width:64px;height:64px;margin:0 auto 14px;border-radius:22px;display:grid;place-items:center;background:color-mix(in srgb,var(--brand) 12%,var(--surface));color:var(--brand);opacity:.85}
.nempty b{display:block;font-size:15px;font-weight:900}
.nempty small{display:block;font-size:12.5px;color:var(--muted);margin-top:8px;line-height:1.9}


.hdr-userui{display:flex;align-items:center;justify-content:center;width:100%;margin-top:14px;padding:11px 16px;border-radius:16px;border:1.5px solid rgba(255,255,255,.5);background:rgba(255,255,255,.18);color:#fff;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;backdrop-filter:blur(6px);white-space:nowrap;box-sizing:border-box}
.hdr-userui:active{transform:scale(.98);background:rgba(255,255,255,.28)}

/* نوار مشاهدهٔ ادمین — داخل خود اپ، نه بیرون صفحه */
.viewas-strip{display:none;align-items:center;justify-content:space-between;gap:10px;margin:0;padding:10px 16px;padding-top:calc(10px + env(safe-area-inset-top));background:linear-gradient(135deg,#6B4EE6,#4B2FD0);color:#fff;position:sticky;top:0;z-index:30;box-sizing:border-box;width:100%}
.viewas-strip.on{display:flex}
.viewas-strip span{font-size:13px;font-weight:800;white-space:nowrap}
.viewas-strip button{flex:none;background:#fff;color:#4B2FD0;border:0;border-radius:12px;padding:8px 14px;font:inherit;font-size:12.5px;font-weight:800;cursor:pointer;white-space:nowrap}
.viewas-strip button:active{transform:scale(.97)}
body.has-viewas .viewas-strip{display:none!important}
.fp-btn{display:flex!important;align-items:center;justify-content:center;gap:10px}
.fp-btn svg{flex:none}
.unlock-card{text-align:center;padding-top:28px!important;padding-bottom:28px!important}
.unlock-name{font-size:18px;font-weight:900;margin-bottom:22px;color:var(--ink)}
.unlock-main{height:56px!important;font-size:16px!important;border-radius:16px!important}
.unlock-hint{margin-top:16px;font-size:12.5px;color:var(--muted);line-height:1.8}
.fp-home{
  margin:16px 20px 0;padding:14px 16px;border-radius:22px;
  background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow);
  display:flex;align-items:center;gap:12px;
}
.fp-home-txt{flex:1;min-width:0;text-align:start}
.fp-home-txt b{display:block;font-size:14px;font-weight:900;color:var(--ink);line-height:1.4}
.fp-home-txt span{display:block;font-size:11.5px;color:var(--muted);line-height:1.45;margin-top:2px}
.fp-home .fp-switch{flex:none}
.fp-switch{display:inline-flex;align-items:center;cursor:pointer;user-select:none;position:relative}
.fp-switch input{position:absolute;opacity:0;width:0;height:0}
.fp-switch-ui{width:46px;height:28px;border-radius:99px;background:#D4D0EA;position:relative;transition:.2s;flex:none}
.fp-switch-ui::after{content:"";position:absolute;top:3px;inset-inline-start:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.15);transition:.2s}
.fp-switch input:checked+.fp-switch-ui{background:var(--brand)}
.fp-switch input:checked+.fp-switch-ui::after{inset-inline-start:21px}
.fp-switch input:disabled+.fp-switch-ui{opacity:.45}
.fp-toggle-box{display:none!important}
.fp-switch{display:flex;align-items:flex-start;gap:8px;cursor:pointer;user-select:none}
.fp-switch input{position:absolute;opacity:0;width:0;height:0}
.fp-switch-ui{flex:none;width:40px;height:22px;border-radius:99px;background:rgba(255,255,255,.25);position:relative;transition:.2s;margin-top:2px}
.fp-switch-ui::after{content:"";position:absolute;top:3px;inset-inline-start:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:.2s}
.fp-switch input:checked+.fp-switch-ui{background:#22c55e}
.fp-switch input:checked+.fp-switch-ui::after{inset-inline-start:21px}
.fp-switch-txt{font-size:10px;line-height:1.35;font-weight:700;color:#fff;text-align:start;opacity:.95}
.au{position:relative}
/* ===== splash ===== */
#splash{position:fixed;inset:0;z-index:100;display:grid;place-items:center;text-align:center;color:#fff;transition:opacity .55s ease,visibility .55s ease;
  background:radial-gradient(rgba(255,255,255,.1) 1.5px,transparent 1.6px) 0 0/18px 18px,linear-gradient(165deg,var(--brand),var(--brand2))}
#splash .sp-logo{display:block;margin:0 auto 8px}
#splash .sp-inner{display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;padding:0 24px;box-sizing:border-box}
#splash.off{opacity:0;visibility:hidden;pointer-events:none}
#splash path{stroke-dasharray:140;stroke-dashoffset:140;animation:draw 1.1s ease-out forwards}
#splash path+path{animation-delay:.28s}
#splash b{display:block;font-size:48px;font-weight:900;margin-top:14px;line-height:1.15;opacity:0;animation:spFade .55s .75s forwards;text-align:center}
#splash small{display:block;margin:4px auto 0;opacity:0;font-size:14px;font-weight:700;letter-spacing:.28em;animation:spFade .55s .95s forwards;text-align:center;direction:ltr;unicode-bidi:isolate}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes spFade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#splash path{stroke-dashoffset:0;animation:none}#splash b,#splash small{opacity:1;animation:none}}

/* ================= v5 ================= */
textarea{font:inherit;color:inherit}
textarea.inp{height:auto;min-height:92px;padding:12px 16px;resize:vertical;line-height:1.9}
a.lr{text-decoration:none;color:inherit}
.lgf{display:grid;place-items:center;border-radius:28%;color:#fff;font-weight:900;background:linear-gradient(135deg,var(--c1),var(--c2));flex:none}
.top.adm{--tc:#2B1F7A;--tc2:#0F0B33}
/* فقط هدر داشبورد ادمین تمام عرض نمایشگر است؛ عرض سایر صفحه‌ها تغییر نمی‌کند. */
.app.admin-wide{overflow-x:visible}
.top.adm.dashboard-head{width:100vw;max-width:none;position:relative;left:auto;transform:none;margin-inline:calc((100% - 100vw)/2)}
.dashboard-head .ph .tt{min-width:0}
.dashboard-head .ph .tt b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dashboard-head .hdr-userui{width:auto;max-width:100%;margin:12px auto 0 0;padding:9px 16px;display:flex;flex:none}
.admin-return{width:auto!important;max-width:44vw;min-width:max-content;height:44px;padding:0 12px!important;border-radius:14px!important;background:#fff!important;color:#4B2FD0!important;font-size:12px!important;font-weight:900!important;white-space:nowrap;flex:none;box-shadow:0 4px 12px rgba(20,10,70,.16)}
.adm-b{display:inline-flex;align-items:center;gap:5px;background:linear-gradient(135deg,#FFD24A,#F3A000);color:#3a2300;font-size:11px;font-weight:900;border-radius:99px;padding:1px 10px;letter-spacing:.5px;margin-top:4px}
.ph .ib{margin-inline-start:auto}

/* ----- status filter bar ----- */
.fbar{margin:-62px 16px 0;position:relative;background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:8px;box-shadow:var(--lift);display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.fbar::-webkit-scrollbar{display:none}
.fc{flex:none;display:flex;align-items:center;gap:7px;padding:9px 14px;border-radius:20px;font-weight:800;font-size:13px;color:var(--muted);background:var(--surface2);white-space:nowrap;border:2px solid transparent;transition:background .2s,color .2s}
.fc i.dot{width:10px;height:10px;border-radius:50%;background:var(--sc);box-shadow:0 0 0 1px var(--muted)}
.fc b{font-size:12px;opacity:.85}
.fc[aria-pressed="true"]{background:var(--sc);color:var(--st);box-shadow:0 10px 16px -10px var(--sc)}
.fc[aria-pressed="true"] i.dot{background:var(--st);box-shadow:none}
.fc.wh[aria-pressed="true"]{background:#fff;color:#17133A;border-color:var(--brand)}
.fc.wh[aria-pressed="true"] i.dot{background:var(--brand)}
.fc.tkc{--sc:var(--brand);--st:#fff}

/* ----- pass (ticket-style cards) ----- */
.pass{margin:14px 16px 0;background:var(--surface);border:1px solid var(--line);border-radius:28px;box-shadow:var(--shadow);position:relative;overflow:hidden;--sc:#3B82F6;--st:#fff;text-align:start;display:block;width:calc(100% - 32px)}
.pass[data-act]{cursor:pointer}
.pass[data-act]:active{transform:scale(.99)}
.pass-top{display:flex;align-items:center;gap:12px;padding:14px 16px 20px;background:linear-gradient(135deg,var(--sc),color-mix(in srgb,var(--sc) 70%,#000));color:var(--st);position:relative;overflow:hidden}
.pass-top::after{content:"";position:absolute;inset-inline-end:-30px;top:-40px;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.14);pointer-events:none}
.pass.wh .pass-top{background:#fff;color:#17133A}
.pass.wh .pass-top::after{background:rgba(107,78,230,.08)}
.pass-lg{width:46px;height:46px;border-radius:15px;background:rgba(255,255,255,.2);display:grid;place-items:center;flex:none;position:relative;z-index:1}
.pass.wh .pass-lg{background:var(--surface2)}
.pass-lg .lgf,.pass-lg .logo{filter:none}
.pass-t{flex:1;min-width:0;position:relative;z-index:1}
.pass-t b{display:block;font-size:17px;font-weight:900;line-height:1.5}
.pass-t small{display:block;font-size:11.5px;opacity:.85;overflow-wrap:anywhere;line-height:1.6}
.spill{flex:none;position:relative;z-index:1;font-size:12px;font-weight:800;border-radius:99px;padding:3px 12px;background:rgba(255,255,255,.24);white-space:nowrap}
.pass.wh .spill{background:var(--surface2);box-shadow:inset 0 0 0 1px var(--line)}
.pass-cut{position:relative;height:0;border-top:2px dashed var(--line);margin:0 24px}
.pass-cut::before,.pass-cut::after{content:"";position:absolute;top:-12px;width:22px;height:22px;border-radius:50%;background:var(--bg)}
.pass-cut::before{inset-inline-start:-36px;box-shadow:inset 0 0 0 1px var(--line)}
.pass-cut::after{inset-inline-end:-36px;box-shadow:inset 0 0 0 1px var(--line)}
.pass-body{padding:16px}
.pass-ti{display:block;font-size:14.5px;font-weight:800;line-height:1.8}
.pass-u{display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:12.5px;font-weight:800}
.pass-u img{width:26px;height:26px;border-radius:50%;object-fit:cover}
.pass-u small{color:var(--muted);font-weight:500;margin-inline-start:auto;font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:50%}
.pg2{display:flex;align-items:center;gap:12px;margin-top:12px}
.pg2-n{font-size:24px;font-weight:900;min-width:64px;color:var(--ink);line-height:1.2}
.pbar{flex:1;height:12px;border-radius:9px;background:var(--surface2);overflow:hidden}
.pbar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,var(--sc),color-mix(in srgb,var(--sc) 65%,#fff));width:var(--p);transition:width .6s}
.pass.wh .pbar i{background:linear-gradient(90deg,var(--brand),var(--brand2))}
.pg2-s{font-size:12px;color:var(--muted);margin-top:6px}
.ord-lk{display:flex;align-items:center;gap:8px;direction:ltr;background:var(--surface2);border-radius:14px;padding:8px 12px;margin-top:12px;font-size:12px;color:var(--muted)}
.ord-lk svg{flex:none}.ord-lk span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;text-align:left}
.onote{display:flex;gap:8px;align-items:flex-start;background:var(--coin-soft);color:var(--ink);border-radius:14px;padding:8px 12px;margin-top:10px;font-size:12.5px;line-height:1.8}
.onote svg{flex:none;margin-top:5px;color:var(--warn)}
.onote.rf{background:color-mix(in srgb,#F97316 14%,var(--surface))}
.pass-f{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:12px;font-weight:900;font-size:16px}
.pass-f small{font-weight:500;font-size:11px;color:var(--muted)}
.pass-f .hint{font-size:11.5px;font-weight:700;color:var(--muted);display:flex;align-items:center;gap:5px}
.newp{background:var(--bad);color:#fff;border-radius:99px;font-size:11px;font-weight:800;padding:0 9px}
.oa{display:flex;gap:8px;margin-top:12px}
.oa button{flex:1;height:44px;border-radius:15px;background:var(--surface2);font-size:12.5px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:6px}
.oa button.pri{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff}
.oa button:active{background:var(--line)}
.pv{margin-top:8px;font-size:13px;color:var(--muted);line-height:1.8;overflow-wrap:anywhere}
.pv b{color:var(--ink);font-weight:800}

/* ----- tickets list ----- */
.tkh{margin:-62px 16px 0;position:relative;background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:16px;box-shadow:var(--lift)}
.tkh-r{display:flex;align-items:center;gap:14px}
.tkh-r .t{flex:1;min-width:0}.tkh-r b{display:block;font-size:15px;font-weight:900}.tkh-r small{color:var(--muted);font-size:12px}
.slots{display:flex;gap:6px;margin-top:6px}.slots i{width:34px;height:8px;border-radius:9px;background:var(--surface2)}.slots i.on{background:linear-gradient(90deg,var(--brand),var(--brand2))}
.tkh .btn{height:50px;margin-top:14px;font-size:15px}
.tkfb{margin:12px 16px 0;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.tkfb::-webkit-scrollbar{display:none}

/* ----- chat overlay ----- */
.tkv{position:fixed;inset:0;z-index:40;display:none;justify-content:center;background:var(--bg)}
.tkv.on{display:flex}
.tkv-in{width:100%;max-width:430px;display:flex;flex-direction:column;height:100%;background:var(--bg)}
.tkv-h{flex:none;color:#fff;padding:calc(env(safe-area-inset-top) + 14px) 14px 16px;display:flex;align-items:center;gap:10px;border-radius:0 0 30px 30px;
  background:radial-gradient(circle at 12% 0%,rgba(255,255,255,.2) 0 70px,transparent 71px),radial-gradient(rgba(255,255,255,.1) 1.5px,transparent 1.6px) 0 0/18px 18px,linear-gradient(165deg,var(--brand),var(--brand2))}
.tkv-h.adm{background:radial-gradient(circle at 12% 0%,rgba(255,255,255,.14) 0 70px,transparent 71px),radial-gradient(rgba(255,255,255,.08) 1.5px,transparent 1.6px) 0 0/18px 18px,linear-gradient(165deg,#2B1F7A,#0F0B33)}
.tkv-h .tt{flex:1;min-width:0}
.tkv-h b{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:15px;line-height:1.6;overflow-wrap:anywhere}
.tkv-h small{display:block;opacity:.85;font-size:11.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tkv-meta{flex:none;display:flex;gap:6px;flex-wrap:wrap;padding:12px 16px 0;align-items:center}
.cx{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:700;background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:3px 10px;max-width:100%}
button.cx{color:var(--brand);border-color:var(--brand)}
.spill2{font-size:12px;font-weight:800;border-radius:99px;padding:3px 12px;background:var(--sc);color:var(--st)}
.tkv-body{flex:1;min-height:0;overflow-y:auto;padding:14px 16px;display:flex;flex-direction:column;gap:10px;overscroll-behavior:contain}
.bub{max-width:82%;padding:9px 14px 5px;border-radius:20px;font-size:14px;line-height:1.9;overflow-wrap:anywhere;white-space:pre-wrap}
.bub small{display:block;font-size:10.5px;opacity:.7;line-height:1.6;margin-top:1px;text-align:end}
.bub.me{align-self:flex-end;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-end-end-radius:6px}
.bub.them{align-self:flex-start;background:var(--surface);border:1px solid var(--line);border-end-start-radius:6px}
.sysm{align-self:center;max-width:90%;text-align:center;font-size:11.5px;color:var(--muted);background:var(--surface2);border-radius:99px;padding:4px 14px;line-height:1.8}
.tkv-closed{flex:none;display:flex;gap:8px;align-items:flex-start;margin:0 12px 8px;background:var(--coin-soft);color:var(--warn);border-radius:16px;padding:8px 12px;font-size:12px;font-weight:700;line-height:1.8}
.tkv-closed svg{flex:none;margin-top:4px}
.tkv-bar{flex:none;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:var(--surface);border-top:1px solid var(--line)}
.qr{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin-bottom:8px}
.qr::-webkit-scrollbar{display:none}
.qr button{flex:none;background:var(--surface2);border:1px solid var(--line);border-radius:99px;padding:3px 12px;font-size:12px;font-weight:800;white-space:nowrap}
.tkv-row{display:flex;gap:8px;align-items:flex-end}
.tkv-row textarea.inp{min-height:48px;max-height:130px;height:48px;padding:11px 16px;border-radius:20px;resize:none;flex:1}
.send{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;display:grid;place-items:center;flex:none;box-shadow:0 10px 16px -10px var(--brand)}
.send svg{transform:scaleX(-1)}
.catc{display:flex;gap:6px;flex-wrap:wrap}
.catc button{background:var(--surface2);border:2px solid var(--line);border-radius:99px;padding:5px 14px;font-size:13px;font-weight:800;color:var(--muted)}
.catc button[aria-pressed="true"]{background:var(--brand);border-color:var(--brand);color:#fff}
.tkrow{display:flex;align-items:center;gap:10px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:10px 12px;margin-top:8px}
.tkrow .t{flex:1;min-width:0;font-size:13px;font-weight:800;overflow-wrap:anywhere}
.tkrow button{background:var(--bad);color:#fff;border-radius:12px;padding:4px 14px;font-weight:800;font-size:12.5px}

/* ----- wallet bits ----- */
.chip[aria-pressed="true"]{border-color:var(--brand);background:color-mix(in srgb,var(--brand) 10%,var(--surface));color:var(--brand)}
.wnote{margin:12px 20px 0;display:flex;gap:8px;align-items:flex-start;font-size:12px;color:var(--muted);background:var(--surface);border:1px dashed var(--line);border-radius:18px;padding:10px 14px;line-height:1.9}
.wnote svg{flex:none;margin-top:5px;color:var(--brand)}
.wbtns{display:grid;gap:10px;margin:14px 20px 0}
.btn.dis{opacity:.5;pointer-events:none}

/* ----- admin ----- */
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:-62px 16px 0;position:relative}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:26px;padding:14px;text-align:start;box-shadow:var(--lift);position:relative;overflow:hidden;display:block}
.kpi::after{content:"";position:absolute;inset-inline-end:-24px;top:-24px;width:84px;height:84px;border-radius:50%;background:color-mix(in srgb,var(--k) 16%,transparent)}
.kpi-i{width:40px;height:40px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb,var(--k) 16%,var(--surface));color:var(--k);position:relative;z-index:1}
.kpi b{display:block;font-size:24px;font-weight:900;line-height:1.4;margin-top:8px;overflow-wrap:anywhere}
.kpi small{color:var(--muted);font-size:12px}
.sbars{display:grid;gap:11px;padding:16px}
.sbr{display:grid;grid-template-columns:104px 1fr 30px;gap:8px;align-items:center;font-size:12.5px;font-weight:700}
.sbr span:first-child{display:flex;align-items:center;gap:6px;white-space:nowrap}
.sbr i.dot{width:10px;height:10px;border-radius:50%;background:var(--sc);box-shadow:0 0 0 1px var(--muted);flex:none}
.sbr .tr{height:10px;border-radius:9px;background:var(--surface2);overflow:hidden}
.sbr .tr b{display:block;height:100%;border-radius:9px;background:var(--sc);box-shadow:0 0 0 1px var(--line) inset}
.sbr span:last-child{text-align:end}
.cr{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;text-align:start}
.cr+.cr{border-top:1px solid var(--line)}
.cr .t{flex:1;min-width:0}.cr .t b{display:block;font-size:13.5px;font-weight:800;line-height:1.7}.cr .t small{color:var(--muted);font-size:11.5px;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cr .lg{width:40px;height:40px;flex:none;display:grid;place-items:center}
.cr .spill{background:var(--sc);color:var(--st);padding:2px 10px;font-size:11.5px}
.cr .spill.wh{background:#fff;color:#17133A;box-shadow:inset 0 0 0 1px var(--line)}
.sch{margin:-62px 16px 0;position:relative}
.sch .fi .inp{height:54px;border-radius:20px;background:var(--surface);box-shadow:var(--lift)}
.urow{display:flex;align-items:center;gap:12px;width:100%;background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:12px;margin-top:10px;text-align:start;box-shadow:var(--shadow)}
.urow img{width:48px;height:48px;border-radius:50%;object-fit:cover;flex:none}
.urow .t{flex:1;min-width:0}.urow b{display:block;font-size:14.5px;font-weight:800;line-height:1.6;overflow-wrap:anywhere}.urow small{display:block;color:var(--muted);font-size:11.5px;direction:ltr;text-align:right;overflow:hidden;text-overflow:ellipsis}
.urow .bl{flex:none;text-align:end;font-weight:900;font-size:14px;color:var(--ok);line-height:1.4}.urow .bl small{direction:rtl;font-weight:500;color:var(--muted)}
.ulist{margin:6px 16px 0}
.uhero{display:flex;align-items:center;gap:14px}
.uhero img{width:66px;height:66px;border-radius:50%;object-fit:cover;border:3px solid var(--line)}
.uhero b{display:block;font-size:17px;line-height:1.5;overflow-wrap:anywhere}.uhero small{display:block;color:var(--muted);direction:ltr;text-align:right;font-size:12px}
.badj{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:14px;margin-top:14px}
.badj .two{margin-top:12px}
.btn.ok{background:linear-gradient(135deg,#22C55E,#0E9F78);color:#fff;box-shadow:0 12px 20px -12px #0E9F78}
.btn.no{background:linear-gradient(135deg,#FF7B9B,#E5476F);color:#fff;box-shadow:0 12px 20px -12px #E5476F}
.btn.sm{height:48px;font-size:14px}
.stg2{display:flex;flex-wrap:wrap;gap:8px}
.stg2 button{display:flex;align-items:center;gap:7px;padding:8px 14px;border-radius:99px;font-size:13px;font-weight:800;background:var(--surface2);border:2px solid var(--line);color:var(--muted)}
.stg2 button i.dot{width:10px;height:10px;border-radius:50%;background:var(--sc);box-shadow:0 0 0 1px var(--muted)}
.stg2 button[aria-pressed="true"]{background:var(--sc);color:var(--st);border-color:var(--sc)}
.stg2 button.wh[aria-pressed="true"]{background:#fff;color:#17133A;border-color:var(--brand)}
.stg2 button[aria-pressed="true"] i.dot{background:var(--st);box-shadow:none}
.stg2 button.wh[aria-pressed="true"] i.dot{background:var(--brand)}
.sec3{display:flex;align-items:center;justify-content:space-between;margin:24px 20px 12px;gap:10px}
.sec3 h2{font-size:17px;font-weight:900}
.mini2{width:36px;height:36px;border-radius:12px;background:var(--surface2);display:grid;place-items:center;flex:none;color:var(--ink)}
.mini2.red{color:var(--bad)}.mini2.pri{background:var(--brand);color:#fff}
.sw{width:40px;height:40px;border-radius:50%;border:3px solid var(--surface);box-shadow:0 0 0 2px var(--line)}
.sw.on{box-shadow:0 0 0 3px var(--ink)}
.swr{display:flex;gap:10px;flex-wrap:wrap}
.clr{width:100%;height:54px;border-radius:16px;padding:3px;border:2px solid var(--line);background:var(--surface2)}
.am{margin:0 16px 12px;background:var(--surface);border:1px solid var(--line);border-radius:26px;box-shadow:var(--shadow);overflow:hidden}
.am-h{display:flex;align-items:center;gap:12px;padding:12px 14px;width:100%;text-align:start}
.am-h .t{flex:1;min-width:0}.am-h b{display:block;font-size:15px;font-weight:900}.am-h small{color:var(--muted);font-size:11.5px}
.am-h .cd{display:flex;gap:4px}.am-h .cd i{width:12px;height:12px;border-radius:50%}
.am-b{display:none;padding:2px 12px 14px}
.am.open .am-b{display:block}
.am.open .am-h .chv{transform:rotate(-90deg)}
.am-h .chv{transition:transform .3s;color:var(--muted)}
.ac{background:var(--surface2);border-radius:20px;padding:10px;margin-top:10px}
.ac-h{display:flex;align-items:center;gap:8px;padding:2px 4px 8px}
.ac-h b{flex:1;font-size:13.5px;font-weight:900;min-width:0;overflow-wrap:anywhere}
.ai{display:flex;align-items:center;gap:8px;background:var(--surface);border-radius:16px;padding:8px 10px;margin-top:6px}
.ai .t{flex:1;min-width:0}.ai b{display:block;font-size:12.5px;font-weight:700;line-height:1.7;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.ai small{color:var(--muted);font-size:11px}
.addb{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;height:42px;border-radius:14px;border:2px dashed var(--line);color:var(--brand);font-weight:800;font-size:13px;margin-top:8px}
.pickrow{display:flex;align-items:center;gap:14px}
.pickrow .prev{width:84px;height:84px;display:grid;place-items:center;flex:none}
.pickrow .prev .logo-img,.pickrow .prev .logo,.pickrow .prev .lgf{filter:none}

/* ================= v5.1: پرداخت کارت‌به‌کارت ================= */
.pstat{flex:none;font-size:11.5px;font-weight:800;border-radius:99px;padding:2px 11px;background:var(--sc);color:var(--st);white-space:nowrap}
.nav.six{gap:2px;padding:8px 6px}
.nav.six button{font-size:10px;height:56px}
.nav.six button.on{flex:1.25}
.nav.six .badge{inset-inline-end:4px}
.au-hint.warn{background:var(--coin-soft);color:var(--warn);font-weight:700}
.au-hint.warn svg{color:var(--warn)}

/* ----- wallet CTA ----- */
.wcta{margin:16px 20px 0;border-radius:30px;padding:18px;color:#fff;position:relative;overflow:hidden;
  background:radial-gradient(circle at 92% -10%,rgba(255,255,255,.22) 0 110px,transparent 111px),radial-gradient(rgba(255,255,255,.09) 1.3px,transparent 1.4px) 0 0/14px 14px,linear-gradient(135deg,color-mix(in srgb,var(--brand2) 80%,#000),#0F0B33);
  box-shadow:0 24px 34px -22px rgba(20,10,80,.9),inset 0 0 0 1px rgba(255,255,255,.1)}
.wc-h{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.wc-h b{display:block;font-size:16px;font-weight:900;line-height:1.5}.wc-h small{font-size:12px;opacity:.8}
.rng{flex:none;font-size:11px;font-weight:800;background:rgba(255,255,255,.14);border-radius:99px;padding:3px 11px;line-height:1.8;color:#FFD24A}
.wsteps{display:flex;align-items:center;margin:18px 0 16px}
.wst{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:10.5px;font-weight:700;flex:none;width:66px;text-align:center;white-space:nowrap}
.wst i{width:42px;height:42px;border-radius:15px;background:rgba(255,255,255,.14);display:grid;place-items:center;box-shadow:inset 0 0 0 1px rgba(255,255,255,.2)}
.wl{flex:1;height:2px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.5) 0 5px,transparent 5px 10px);margin-bottom:22px}
.wbtn{width:100%;background:linear-gradient(135deg,#FFD24A,#F3A000);color:#3a2300;box-shadow:0 14px 22px -12px #F3A000}

/* ----- pay flow ----- */
.sheet.pf{padding-top:8px}
.pfs{animation:fin .35s ease-out}
.stp{display:flex;align-items:center;margin:2px 6px 16px}
.stp .s{display:flex;flex-direction:column;align-items:center;gap:5px;flex:none;width:66px;font-size:11px;font-weight:800;color:var(--muted);text-align:center;line-height:1.5}
.stp .s i{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--surface2);border:2px solid var(--line);font-style:normal;font-size:15px;font-weight:900;transition:all .3s}
.stp .s.on{color:var(--ink)}
.stp .s.on i{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-color:transparent;box-shadow:0 0 0 5px color-mix(in srgb,var(--brand) 22%,transparent)}
.stp .s.dn i{background:var(--ok);color:#fff;border-color:transparent}
.stp .ln{flex:1;height:4px;border-radius:4px;background:var(--line);margin-bottom:22px;overflow:hidden}
.stp .ln b{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--ok),var(--brand));transition:width .5s}
.stp .ln.dn b{width:100%}
.amtbox{position:relative;margin-top:10px}
.amtbox .inp{height:46px;font-size:15px;font-weight:700;text-align:center;padding-inline:64px 14px;--tc:var(--brand);letter-spacing:.3px}
.amtbox span{position:absolute;inset-inline-end:14px;top:50%;transform:translateY(-50%);color:var(--muted);font-weight:700;font-size:12px}
.payamt{margin:14px 0 12px;background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:12px 16px;text-align:center}
.payamt small{display:block;color:var(--muted);font-size:12px}
.payamt b{font-size:30px;font-weight:900;color:var(--brand);line-height:1.4}.payamt span{font-size:13px;color:var(--muted);font-weight:700}
.bkw{height:204px;margin:6px 0 0}
.bk{position:absolute;inset:0;border-radius:28px;padding:18px 20px;color:#fff;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;
  background:radial-gradient(circle at 90% -10%,color-mix(in srgb,var(--brand) 85%,transparent) 0 130px,transparent 131px),radial-gradient(circle at 0% 115%,rgba(246,168,35,.42) 0 120px,transparent 121px),radial-gradient(rgba(255,255,255,.07) 1.2px,transparent 1.3px) 0 0/14px 14px,linear-gradient(135deg,color-mix(in srgb,var(--brand2) 78%,#000),#0F0B33);
  box-shadow:0 26px 36px -22px rgba(20,10,80,.9),inset 0 0 0 1px rgba(255,255,255,.12)}
.bk::after{content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.2) 44%,rgba(110,200,255,.2) 50%,rgba(255,170,255,.18) 56%,transparent 70%);background-size:260% 100%;background-position:var(--sx,120%) 0;animation:sheen 2.6s .4s 1 both}
.bk-r{display:flex;align-items:center;justify-content:space-between;gap:10px;position:relative;z-index:1}
.bk-l{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:800;opacity:.9}
.bk .mc-chip{position:relative;z-index:1}
.bk-num{position:relative;z-index:1;direction:ltr;text-align:left;font-size:22px;letter-spacing:2.5px;font-weight:800;font-variant-numeric:tabular-nums;text-shadow:0 2px 6px rgba(0,0,0,.4)}
.bk-o{min-width:0}.bk-o small{display:block;font-size:10.5px;opacity:.65}.bk-o b{display:block;font-size:16px;font-weight:900;line-height:1.5}
.bk-c{width:42px;height:42px;border-radius:14px;background:rgba(255,255,255,.18);display:grid;place-items:center;flex:none;color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)}
.warnc{background:var(--coin-soft);border:1px solid color-mix(in srgb,var(--warn) 35%,transparent);border-radius:18px;padding:12px 14px;margin-top:12px;font-size:12.5px;line-height:2;color:var(--ink);font-weight:600}
.up{display:flex;flex-direction:column;align-items:center;gap:4px;width:100%;padding:22px 12px;border:2px dashed var(--brand);border-radius:24px;background:color-mix(in srgb,var(--brand) 6%,var(--surface));color:var(--brand);margin-top:8px}
.up b{font-size:15px;font-weight:900}.up small{color:var(--muted);font-size:12px}
.upv{margin-top:8px}.upv img{width:100%;max-height:260px;object-fit:contain;border-radius:20px;background:var(--surface);border:1px solid var(--line);display:block}
.upv .two{margin-top:8px}
.ck{display:flex;gap:10px;align-items:flex-start;margin-top:12px;font-size:13px;font-weight:700;line-height:1.8}
.ck input{width:22px;height:22px;accent-color:var(--brand);flex:none;margin-top:3px}
.done{text-align:center;padding:6px 4px 0}
.done svg circle{stroke-dasharray:150;stroke-dashoffset:150;animation:draw 1s ease-out forwards}
.done svg path{stroke-dasharray:50;stroke-dashoffset:50;animation:draw .6s .6s ease-out forwards}
.done b{display:block;font-size:22px;font-weight:900;margin-top:8px}
.done p{color:var(--muted);font-size:13.5px;line-height:2;margin:6px 0 14px}
.payid{background:var(--surface);border:1px dashed var(--brand);border-radius:16px;padding:8px 14px;margin-bottom:14px;font-size:13px;color:var(--muted)}.payid b{display:inline;font-size:15px;color:var(--brand);margin:0}

/* ----- admin payments ----- */
.payrow{display:flex;gap:12px;align-items:center;margin-top:4px}
.payrow .thumb{width:62px;height:62px;border-radius:16px;object-fit:cover;flex:none;border:1px solid var(--line);background:var(--surface2)}
.payrow .ph0{display:grid;place-items:center;color:var(--muted)}
.payrow .t{min-width:0;flex:1}.payrow .amt{font-size:20px;font-weight:900;line-height:1.5}.payrow .amt small{font-size:12px;color:var(--muted);font-weight:600}
.rcpt{width:100%;max-height:300px;object-fit:contain;border-radius:20px;background:var(--surface);border:1px solid var(--line);display:block;margin-bottom:10px;cursor:zoom-in}
#zoom{position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.88);display:none;align-items:center;justify-content:center;padding:12px}
#zoom.on{display:flex}
#zoom img{max-width:100%;max-height:100%;object-fit:contain;border-radius:12px}

/* ----- قفل دستگاه ----- */
.au.lockup .seg2,.au.lockup .form.up{display:none}
.au-ttl{text-align:center;margin-bottom:4px}.au-ttl b{display:block;font-size:19px;font-weight:900}.au-ttl small{display:block;color:var(--muted);font-size:12px;line-height:1.9;margin-top:2px}
/* au-ttl always visible */
.au.lockup .form{margin-top:12px}

.mact{display:flex;gap:12px;margin-top:4px}.mact button{font-size:11px;opacity:.85;text-decoration:underline}
.bkrow{display:flex;align-items:center;gap:8px;padding:10px 0;border-top:1px solid var(--line)}.bkrow .t{flex:1;min-width:0;font-size:13px}
.bkrow button{font-size:12px;padding:6px 10px;border-radius:10px;background:var(--surface2)}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <linearGradient id="cRim" x1=".15" y1="0" x2=".85" y2="1"><stop offset="0" stop-color="#fff3b0"/><stop offset=".4" stop-color="#ffc83a"/><stop offset="1" stop-color="#d47800"/></linearGradient>
  <linearGradient id="cFace" x1=".2" y1="0" x2=".8" y2="1"><stop offset="0" stop-color="#ffd24a"/><stop offset="1" stop-color="#f3a000"/></linearGradient>
  <linearGradient id="gBale" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2ED8A7"/><stop offset="1" stop-color="#0A8560"/></linearGradient>
  <linearGradient id="gEitaa" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFA24A"/><stop offset="1" stop-color="#E0620A"/></linearGradient>
  <linearGradient id="gRubika" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0509F"/><stop offset="1" stop-color="#A3166A"/></linearGradient>
  <linearGradient id="gTg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#37B6F5"/><stop offset="1" stop-color="#1779B5"/></linearGradient>
  <linearGradient id="gIg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FEDA75"/><stop offset=".3" stop-color="#FA7E1E"/><stop offset=".6" stop-color="#D62976"/><stop offset=".8" stop-color="#962FBF"/><stop offset="1" stop-color="#4F5BD5"/></linearGradient>
  <linearGradient id="gYt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF5A5A"/><stop offset="1" stop-color="#C21B1B"/></linearGradient>
  <symbol id="coin" viewBox="0 0 64 64">
    <circle cx="32" cy="34" r="29" fill="#b45f00"/><circle cx="32" cy="31.5" r="29" fill="url(#cRim)"/>
    <circle cx="32" cy="31.5" r="26.6" fill="none" stroke="#a85900" stroke-opacity=".28" stroke-width="2" stroke-dasharray="1.4 2.01"/>
    <circle cx="32" cy="31.5" r="22.4" fill="url(#cFace)" stroke="#c77200" stroke-width="1.6"/>
    <path d="M22 42V32a10 10 0 0 1 20 0v10" fill="none" stroke="#fffbe3" stroke-width="4" stroke-linecap="round" transform="translate(0 .8)" opacity=".55"/>
    <path d="M22 42V32a10 10 0 0 1 20 0v10" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" transform="translate(0 -.8)"/>
    <path d="M28 42V33a4 4 0 0 1 8 0v9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" transform="translate(0 -.8)" opacity=".8"/>
    <path d="M13.5 26c1.9-6.2 7-10.4 13.2-11.4" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="2.6" stroke-linecap="round"/>
  </symbol>
  <symbol id="lg-bale" viewBox="0 0 48 48"><rect width="48" height="48" rx="14" fill="url(#gBale)"/><path d="M24 11c7.7 0 13 4.9 13 11s-5.3 11-13 11c-1.5 0-2.9-.2-4.2-.6L13 36l1.5-5.6C12.3 28.6 11 25.5 11 22c0-6.1 5.3-11 13-11z" fill="#fff"/><path d="M18.5 22l4 4 7.5-7.5" fill="none" stroke="#0A8560" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="lg-eitaa" viewBox="0 0 48 48"><rect width="48" height="48" rx="14" fill="#FF7634"/><path fill="#fff" fill-rule="evenodd" d="M22.01 43.92C21.46 43.94 20.49 43.96 19.87 43.92C19.24 43.89 18.86 43.85 18.26 43.74C17.65 43.62 16.81 43.41 16.21 43.23C15.62 43.04 15.25 42.89 14.71 42.64C14.17 42.38 13.48 42.00 12.99 41.70C12.51 41.40 12.21 41.17 11.81 40.84C11.42 40.51 11.03 40.17 10.63 39.73C10.23 39.30 9.76 38.71 9.41 38.23C9.07 37.74 8.84 37.37 8.56 36.83C8.27 36.30 7.97 35.67 7.72 35.01C7.47 34.34 7.23 33.54 7.06 32.86C6.90 32.18 6.80 31.46 6.73 30.93C6.65 30.39 6.63 30.28 6.61 29.64C6.59 28.99 6.57 27.92 6.63 27.06C6.69 26.20 6.84 25.20 6.96 24.48C7.08 23.77 7.21 23.36 7.37 22.77C7.53 22.17 7.70 21.58 7.93 20.94C8.16 20.30 8.43 19.61 8.76 18.90C9.08 18.19 9.50 17.38 9.88 16.70C10.26 16.02 10.66 15.40 11.05 14.82C11.44 14.24 11.68 13.86 12.22 13.21C12.76 12.55 13.63 11.55 14.28 10.88C14.93 10.21 15.55 9.68 16.11 9.20C16.66 8.73 17.09 8.40 17.61 8.03C18.13 7.65 18.54 7.35 19.22 6.96C19.90 6.57 20.96 6.00 21.69 5.66C22.43 5.32 22.98 5.12 23.62 4.90C24.27 4.68 24.95 4.51 25.56 4.36C26.17 4.22 26.63 4.12 27.28 4.05C27.92 3.98 28.76 3.94 29.42 3.94C30.09 3.94 30.68 3.99 31.25 4.06C31.82 4.13 32.36 4.25 32.86 4.38C33.36 4.50 33.81 4.64 34.26 4.81C34.70 4.98 35.13 5.18 35.54 5.40C35.95 5.62 36.34 5.86 36.72 6.12C37.09 6.38 37.46 6.68 37.78 6.98C38.11 7.28 38.44 7.64 38.69 7.95C38.95 8.25 39.10 8.44 39.33 8.81C39.55 9.17 39.85 9.70 40.05 10.13C40.25 10.56 40.40 10.98 40.53 11.38C40.65 11.79 40.74 12.12 40.82 12.56C40.90 13.01 40.96 13.49 40.98 14.07C41.00 14.64 40.97 15.46 40.93 16.00C40.88 16.54 40.82 16.82 40.72 17.29C40.61 17.75 40.44 18.36 40.30 18.79C40.17 19.22 40.06 19.47 39.88 19.87C39.70 20.26 39.47 20.72 39.22 21.15C38.97 21.58 38.65 22.05 38.36 22.44C38.07 22.84 37.83 23.15 37.50 23.52C37.18 23.89 36.78 24.30 36.40 24.65C36.03 25.01 35.69 25.31 35.26 25.66C34.83 26.02 34.32 26.42 33.83 26.77C33.34 27.12 32.91 27.40 32.32 27.75C31.73 28.11 31.23 28.43 30.28 28.92C29.33 29.41 27.47 30.24 26.63 30.69C25.79 31.14 25.59 31.36 25.23 31.63C24.88 31.89 24.78 31.98 24.48 32.28C24.19 32.57 23.76 33.03 23.47 33.40C23.18 33.76 23.00 34.00 22.74 34.47C22.47 34.94 22.10 35.65 21.88 36.19C21.66 36.72 21.51 37.43 21.41 37.69C21.30 37.95 21.30 37.76 21.26 37.77C21.22 37.77 21.39 37.93 21.15 37.73C20.92 37.52 20.21 36.93 19.87 36.55C19.52 36.17 19.30 35.80 19.09 35.44C18.88 35.07 18.75 34.79 18.62 34.36C18.50 33.93 18.37 33.29 18.32 32.86C18.28 32.43 18.26 32.27 18.34 31.79C18.41 31.30 18.62 30.44 18.78 29.96C18.94 29.48 19.09 29.24 19.30 28.89C19.52 28.53 19.94 28.01 20.06 27.81C20.19 27.62 20.22 27.90 20.05 27.70C19.89 27.51 19.31 26.92 19.08 26.63C18.85 26.34 18.82 26.27 18.68 25.99C18.54 25.70 18.34 25.25 18.23 24.91C18.12 24.57 18.07 24.29 18.04 23.95C18.00 23.61 17.99 23.23 18.03 22.87C18.06 22.51 18.10 22.21 18.22 21.80C18.35 21.39 18.61 20.78 18.79 20.43C18.97 20.07 19.05 19.96 19.30 19.65C19.54 19.34 19.91 18.89 20.26 18.58C20.60 18.26 21.17 17.67 21.37 17.76C21.56 17.85 21.38 18.76 21.43 19.11C21.47 19.47 21.55 19.63 21.65 19.87C21.74 20.10 21.86 20.31 21.99 20.51C22.11 20.71 22.22 20.85 22.42 21.05C22.62 21.25 22.92 21.51 23.19 21.71C23.47 21.91 23.61 22.04 24.05 22.23C24.50 22.43 25.31 22.74 25.88 22.88C26.45 23.03 26.97 23.09 27.49 23.13C28.01 23.17 28.49 23.16 28.99 23.13C29.49 23.09 30.07 23.00 30.50 22.91C30.93 22.82 31.19 22.73 31.57 22.59C31.95 22.45 32.39 22.25 32.75 22.06C33.11 21.86 33.42 21.64 33.72 21.40C34.01 21.17 34.32 20.86 34.53 20.62C34.74 20.38 34.84 20.21 34.98 19.97C35.12 19.74 35.25 19.53 35.35 19.22C35.45 18.92 35.54 18.43 35.57 18.15C35.60 17.86 35.59 17.75 35.56 17.50C35.52 17.25 35.49 16.97 35.35 16.64C35.22 16.32 34.96 15.87 34.73 15.57C34.51 15.27 34.19 15.00 33.98 14.82C33.78 14.64 33.71 14.61 33.50 14.48C33.30 14.34 33.06 14.18 32.75 14.03C32.45 13.89 32.14 13.75 31.68 13.61C31.21 13.46 30.68 13.27 29.96 13.17C29.24 13.07 28.04 13.00 27.38 12.99C26.72 12.97 26.42 13.04 25.99 13.09C25.56 13.14 25.34 13.15 24.81 13.28C24.27 13.40 23.45 13.61 22.77 13.84C22.09 14.07 21.32 14.39 20.72 14.67C20.13 14.95 19.72 15.20 19.22 15.52C18.72 15.83 18.18 16.21 17.72 16.58C17.25 16.94 16.79 17.36 16.43 17.69C16.07 18.03 15.88 18.24 15.57 18.60C15.26 18.96 14.83 19.51 14.57 19.87C14.31 20.22 14.23 20.35 14.01 20.72C13.80 21.10 13.46 21.74 13.29 22.12C13.11 22.50 13.09 22.59 12.96 22.98C12.84 23.37 12.64 23.98 12.54 24.48C12.44 24.98 12.37 25.57 12.34 25.99C12.30 26.40 12.30 26.54 12.33 26.95C12.36 27.36 12.43 28.03 12.52 28.46C12.60 28.89 12.72 29.19 12.84 29.53C12.97 29.87 13.07 30.14 13.27 30.50C13.47 30.85 13.80 31.34 14.06 31.68C14.31 32.01 14.55 32.24 14.82 32.50C15.09 32.76 15.30 32.96 15.68 33.22C16.05 33.49 16.74 33.68 17.07 34.09C17.41 34.49 17.47 35.19 17.69 35.65C17.92 36.11 18.17 36.48 18.43 36.83C18.68 37.18 18.98 37.51 19.22 37.77C19.46 38.03 19.62 38.18 19.87 38.38C20.12 38.58 20.46 38.82 20.72 38.99C20.99 39.16 21.24 39.29 21.48 39.38C21.71 39.48 21.97 39.58 22.12 39.56C22.27 39.55 22.26 39.60 22.37 39.30C22.47 39.01 22.60 38.26 22.73 37.80C22.87 37.34 23.01 36.96 23.19 36.54C23.38 36.12 23.36 35.58 23.84 35.30C24.32 35.03 25.41 35.06 26.09 34.91C26.77 34.76 27.24 34.62 27.92 34.39C28.60 34.16 29.46 33.83 30.17 33.51C30.89 33.19 31.48 32.90 32.21 32.47C32.95 32.05 33.38 31.83 34.58 30.97C35.78 30.11 38.25 28.22 39.41 27.31C40.57 26.40 41.07 25.88 41.56 25.51C42.04 25.14 42.06 25.17 42.31 25.08C42.56 24.99 42.85 24.96 43.06 24.99C43.27 25.01 43.44 25.10 43.59 25.23C43.73 25.37 43.87 25.57 43.92 25.77C43.98 25.97 43.93 26.24 43.90 26.42C43.87 26.60 43.82 26.68 43.74 26.85C43.65 27.01 43.75 26.93 43.38 27.38C43.01 27.83 42.67 28.15 41.53 29.53C40.38 30.91 37.81 34.16 36.53 35.65C35.24 37.15 34.58 37.76 33.83 38.50C33.07 39.23 32.45 39.70 32.00 40.07C31.55 40.44 31.54 40.45 31.14 40.72C30.75 40.98 30.09 41.40 29.63 41.66C29.16 41.93 28.74 42.15 28.35 42.33C27.96 42.52 27.87 42.58 27.28 42.78C26.68 42.98 25.49 43.35 24.81 43.52C24.13 43.70 23.66 43.75 23.19 43.82C22.73 43.88 22.57 43.91 22.01 43.92Z"/></symbol>
  <symbol id="lg-rubika" viewBox="0 0 48 48"><clipPath id="rbClip"><path d="M22.70 4.75Q24.00 4.00 25.30 4.75L40.02 13.25Q41.32 14.00 41.32 15.50L41.32 32.50Q41.32 34.00 40.02 34.75L25.30 43.25Q24.00 44.00 22.70 43.25L7.98 34.75Q6.68 34.00 6.68 32.50L6.68 15.50Q6.68 14.00 7.98 13.25Z"/></clipPath><rect width="48" height="48" rx="14" fill="#fff"/><g clip-path="url(#rbClip)"><path fill="#7EB427" stroke="#7EB427" stroke-width=".12" d="M24.00 4.00L32.66 9.00L24.00 14.00Z"/><path fill="#38AD9C" stroke="#38AD9C" stroke-width=".12" d="M24.00 14.00L32.66 9.00L32.66 19.00Z"/><path fill="#5BD5BD" stroke="#5BD5BD" stroke-width=".12" d="M32.66 9.00L41.32 14.00L32.66 19.00Z"/><path fill="#7A4587" stroke="#7A4587" stroke-width=".12" d="M41.32 14.00L41.32 24.00L32.66 19.00Z"/><path fill="#4D3884" stroke="#4D3884" stroke-width=".12" d="M32.66 19.00L41.32 24.00L32.66 29.00Z"/><path fill="#E54D52" stroke="#E54D52" stroke-width=".12" d="M41.32 24.00L41.32 34.00L32.66 29.00Z"/><path fill="#EE7617" stroke="#EE7617" stroke-width=".12" d="M41.32 34.00L32.66 39.00L32.66 29.00Z"/><path fill="#F4A926" stroke="#F4A926" stroke-width=".12" d="M32.66 29.00L32.66 39.00L24.00 34.00Z"/><path fill="#B8CD06" stroke="#B8CD06" stroke-width=".12" d="M32.66 39.00L24.00 44.00L24.00 34.00Z"/><path fill="#7EB427" stroke="#7EB427" stroke-width=".12" d="M24.00 44.00L15.34 39.00L24.00 34.00Z"/><path fill="#38AD9C" stroke="#38AD9C" stroke-width=".12" d="M24.00 34.00L15.34 39.00L15.34 29.00Z"/><path fill="#5BD5BD" stroke="#5BD5BD" stroke-width=".12" d="M15.34 39.00L6.68 34.00L15.34 29.00Z"/><path fill="#4D3884" stroke="#4D3884" stroke-width=".12" d="M6.68 34.00L6.68 24.00L15.34 29.00Z"/><path fill="#7A4587" stroke="#7A4587" stroke-width=".12" d="M15.34 29.00L6.68 24.00L15.34 19.00Z"/><path fill="#E54D52" stroke="#E54D52" stroke-width=".12" d="M6.68 24.00L6.68 14.00L15.34 19.00Z"/><path fill="#EE7617" stroke="#EE7617" stroke-width=".12" d="M6.68 14.00L15.34 9.00L15.34 19.00Z"/><path fill="#F4A926" stroke="#F4A926" stroke-width=".12" d="M15.34 19.00L15.34 9.00L24.00 14.00Z"/><path fill="#B8CD06" stroke="#B8CD06" stroke-width=".12" d="M15.34 9.00L24.00 4.00L24.00 14.00Z"/><path fill="#FDFDFD" stroke="#FDFDFD" stroke-width=".12" d="M24.00 14.00L32.66 19.00L24.00 24.00L15.34 19.00Z"/><path fill="#E3E3E3" stroke="#E3E3E3" stroke-width=".12" d="M15.34 19.00L24.00 24.00L24.00 34.00L15.34 29.00Z"/><path fill="#EFEFEF" stroke="#EFEFEF" stroke-width=".12" d="M24.00 24.00L32.66 19.00L32.66 29.00L24.00 34.00Z"/></g></symbol>
  <symbol id="lg-tg" viewBox="0 0 48 48"><rect width="48" height="48" rx="14" fill="url(#gTg)"/><path d="M37 11.5 11 21.5l8.500 3 3 9.500 4.800-5.800 7.200 5.300z" fill="#fff"/><path d="M19.500 24.500 33 16" fill="none" stroke="#1779B5" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="lg-ig" viewBox="0 0 48 48"><rect width="48" height="48" rx="14" fill="url(#gIg)"/><rect x="12" y="12" width="24" height="24" rx="8" fill="none" stroke="#fff" stroke-width="3"/><circle cx="24" cy="24" r="5.5" fill="none" stroke="#fff" stroke-width="3"/><circle cx="31" cy="17" r="1.8" fill="#fff"/></symbol>
  <symbol id="lg-yt" viewBox="0 0 48 48"><rect width="48" height="48" rx="14" fill="url(#gYt)"/><rect x="9" y="14" width="30" height="20" rx="7" fill="#fff"/><path d="M21 19v10l9-5z" fill="#D82525"/></symbol>
</defs></svg>

<div id="splash"><div class="sp-inner">
  <img class="sp-logo" src="/logo.jpg" alt="Arka" width="120" height="120" style="border-radius:28px;object-fit:cover;box-shadow:0 20px 40px rgba(0,0,0,.25)">
  <b>آرکا</b>
  <small>Arka</small>
</div></div>
<script>
document.addEventListener('error',function(e){var t=e.target;if(t&&t.classList&&t.classList.contains('sp-logo'))t.style.display='none'},true);
(function(){
  function hideSplash(){
    var s=document.getElementById('splash');
    if(!s)return;
    s.classList.add('off');
    s.style.opacity='0';
    s.style.visibility='hidden';
    s.style.pointerEvents='none';
  }
  setTimeout(hideSplash, 1800);
  setTimeout(hideSplash, 3500);
  setTimeout(hideSplash, 6000);
  window.__hideSplash = hideSplash;
})();
</script>
</canvas>
<div class="toast" id="toast" role="status"></div>

<div id="auth"></div>
<div id="zoom" data-act="zoomx"><img alt=""></div>

<main class="app"><div class="viewas-strip" id="viewasStrip"><span>صفحه کاربران</span><button type="button" data-act="asadmin">بازگشت به ادمین</button></div>
  <section class="view on" id="v-home"></section>
  <section class="view" id="v-plat"></section>
  <section class="view" id="v-orders"></section>
  <section class="view" id="v-tickets"></section>
  <section class="view" id="v-wallet"></section>
  <section class="view" id="v-me"></section>
  <section class="view" id="v-a-dash"></section>
  <section class="view" id="v-a-orders"></section>
  <section class="view" id="v-a-pays"></section>
  <section class="view" id="v-a-tickets"></section>
  <section class="view" id="v-a-users"></section>
  <section class="view" id="v-a-manage"></section>
</main>

<div class="tkv" id="tkv"><div class="tkv-in" id="tkvin"></div></div>
<div class="sbg" id="sbg"><div class="sheet" id="sheet" role="dialog" aria-modal="true"></div></div>
<input type="file" id="pfile" accept="image/*" hidden>

<nav class="nav" aria-label="منوی اصلی" id="nav"></nav>

<script>
/* ============ ذخیره‌سازی (اگر مرورگر اجازه نداد، فقط در حافظه) ============ */
const mem={};
const S={
  g(k){try{const v=localStorage.getItem(k);return v===null?(mem[k]??null):v}catch(e){return mem[k]??null}},
  s(k,v){mem[k]=v;try{localStorage.setItem(k,v);return true}catch(e){return false}},
  d(k){delete mem[k];try{localStorage.removeItem(k)}catch(e){}}
};

/* ===== API (server) ===== */
const API = {
  async get(path, extraHeaders){
    const h=Object.assign({'X-Device':deviceId(),'X-Token':(S.g('arka:token')||''),'X-CSRF':(window.__CSRF||'')},extraHeaders||{});
    const r=await fetch(path,{headers:h,cache:'no-store'});
    const d=await r.json().catch(()=>({}));
    if(!r.ok){const e=new Error(d.detail||('خطا '+r.status));if(d.retry)e.retry=d.retry;if(d.challenge)e.challenge=d.challenge;throw e}
    if(d.csrf)window.__CSRF=d.csrf;
    return d;
  },
  async post(path, body){
    const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Device':deviceId(),'X-Token':(S.g('arka:token')||''),'X-CSRF':(window.__CSRF||'')},body:JSON.stringify(body||{})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok){const e=new Error(d.detail||('خطا '+r.status));if(d.retry)e.retry=d.retry;if(d.challenge)e.challenge=d.challenge;throw e}
    if(d.csrf)window.__CSRF=d.csrf;
    return d;
  }
};
function deviceId(){
  let id=S.g('arka:did');
  if(!id){id='d_'+Math.random().toString(36).slice(2)+Date.now().toString(36);S.s('arka:did',id)}
  return id;
}

const hash=s=>{let a=0xdeadbeef^s.length,b=0x41c6ce57^s.length;for(let i=0;i<s.length;i++){const c=s.charCodeAt(i);a=Math.imul(a^c,2654435761);b=Math.imul(b^c,1597334677)}a=Math.imul(a^a>>>16,2246822507)^Math.imul(b^b>>>13,3266489909);b=Math.imul(b^b>>>16,2246822507)^Math.imul(a^a>>>13,3266489909);return(4294967296*(2097151&b)+(a>>>0)).toString(36)};

/* ============ تنظیمات ثابت ============ */
const ADMIN_EMAIL='manihoseini206@gmail.com';
const BALE={id:'@Arka_Member',url:'https://ble.ir/Arka_Member'};
const ARKA_LOGO='/logo.jpg';
const dev=()=>S.g('arka:device');
const CH_MIN=100000,CH_MAX=10000000,CARD={num:'5892101280721867',name:'سید محمد مانی حسینی'};
const PAYST={pending:{n:'در انتظار بررسی',c:'#F59E0B',tc:'#2B1D00'},ok:{n:'تایید شد',c:'#16A34A',tc:'#FFFFFF'},rejected:{n:'رد شد',c:'#E5476F',tc:'#FFFFFF'}};
const WARN_TXT='⚠️ توجه مهم: لطفاً از ارسال فیش واریزی جعلی خودداری کنید. تمامی پرداخت‌ها بررسی می‌شوند و در صورت مغایرت، سفارش تأیید نخواهد شد. مسئولیت هرگونه تخلف بر عهده کاربر است. 🙏';
const MAXACT=2,DAY=864e5,AUTO=3*DAY;
const ALL={k:'all',n:'همه',c:'#FFFFFF',tc:'#17133A',wh:1};
const STS=[
 {k:'queue',n:'در صف',c:'#3B82F6',tc:'#FFFFFF'},
 {k:'proc',n:'در حال پردازش',c:'#FFFFFF',tc:'#17133A',wh:1},
 {k:'run',n:'در حال انجام',c:'#F0456F',tc:'#FFFFFF'},
 {k:'done',n:'کامل شده',c:'#16A34A',tc:'#FFFFFF'},
 {k:'part',n:'نیمه تمام',c:'#FACC15',tc:'#3A2B00'},
 {k:'cancel',n:'لغو شده',c:'#14B8A6',tc:'#FFFFFF'},
 {k:'refund',n:'بازگشت مبلغ شده',c:'#F97316',tc:'#FFFFFF'},
];
const stMeta=k=>STS.find(s=>s.k===k)||STS[0];
const stStyle=s=>`--sc:${s.c};--st:${s.tc}`;
const TK_CATS=['سفارش','کیف پول','سوال کلی','مشکل فنی'];
const QR=[
 {s:'در حال بررسی',t:'سلام وقت بخیر؛ درخواست شما در حال بررسی است و به‌زودی نتیجه را اطلاع می‌دهیم.'},
 {s:'ارسال لینک و شماره سفارش',t:'لطفاً شماره سفارش و لینک مربوطه را ارسال کنید تا بررسی کنیم.'},
 {s:'موجودی شارژ شد',t:'موجودی کیف پول شما شارژ شد. لطفاً بررسی کنید.'},
 {s:'مشکل برطرف شد',t:'مشکل شما برطرف شد. اگر مورد دیگری بود در خدمتیم.'},
 {s:'سفارش تکمیل شد',t:'سفارش شما تکمیل شد؛ ممنون از اعتماد شما.'}
];
const BRANDS=[['#6B4EE6','#4B2FD0'],['#2563EB','#1E40AF'],['#0E9F78','#0A6B52'],['#E1306C','#9B1F8F'],['#F57C1F','#C95A08'],['#E5476F','#A3173F']];
const SYMS=['bale','eitaa','rubika','tg','ig','yt'];

/* ============ محصولات پیش‌فرض (ادمین می‌تواند ویرایش کند) ============ */
const NOTES=['در زمان ثبت سفارش، از سرویس یا سایت دیگری سفارش ممبر ثبت نکنید.','کانال در حال ریزش نباشد. مسئولیت ریزش ممبرهای قبلی کانال بر عهده مشتری است.','قبل از خرید، موارد بالا را مطالعه کرده و پذیرفته‌اید. در صورت عدم موافقت، سفارش ثبت نکنید.'];
function seedProducts(){
  let n=0;
  const M=(title,rate,min,max,rows,o={})=>({id:'b'+(++n),n:title,rate,min,max,rows,samples:o.samples||[],notes:o.notes===undefined?NOTES:o.notes});
  return [
   {id:'bale',n:'بله',c:'#14B27F',d:'#0A8560',types:[{id:'mem',n:'ممبر کانال و گروه',items:[
    M('ممبر کانال و گروه بله {بدون ریزش 7 روزه} - سرعت کم',273000,500,31000,[['زمان شروع','24 تا 48 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','7 روز بدون ریزش'],['زمان تکمیل','48 تا 72 ساعت'],['لینک','لینک عمومی یا خصوصی کانال یا گروه بله']],{samples:['https://ble.ir/Arka_Member','https://ble.ir/join/Arka_Member']}),
    M('ممبر کانال بله - 7 روز بدون ریزش - سریع',286000,100,17000,[['زمان تکمیل','5 تا 24 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','7 روز بدون ریزش'],['لینک','لینک عمومی یا شناسه کانال']],{samples:['@Arka_Member','https://ble.ir/Arka_Member']}),
    M('ممبر کانال بله {ریزش‌دار}',476800,100,10000,[['زمان شروع','6 تا 24 ساعت'],['زمان تکمیل','1 تا 3 روز'],['میزان ریزش','به دلیل واقعی بودن ممبرها، ریزش نامشخص است.'],['کیفیت سرویس','واقعی'],['فرمت لینک','فقط شناسه کانال']],{samples:['@Arka_Member'],notes:[]}),
    M('ممبر کانال بله {بدون ریزش 1 ماه} - سریع',600000,100,22000,[['زمان تکمیل','6 تا 24 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','30 روز بدون ریزش'],['لینک','لینک عمومی یا شناسه کانال']],{samples:['@Arka_Member','https://ble.ir/Arka_Member']}),
    M('ممبر کانال و گروه بله {بدون ریزش 1 ماه} - سرعت کم',612000,1000,31000,[['زمان شروع','24 تا 48 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','30 روز بدون ریزش'],['زمان تکمیل','48 تا 72 ساعت'],['لینک','لینک عمومی یا خصوصی کانال یا گروه بله']],{samples:['https://ble.ir/Arka_Member','https://ble.ir/join/Arka_Member']}),
    M('ممبر گروه بله {ریزش‌دار}',756000,100,10000,[['زمان شروع','6 تا 24 ساعت'],['زمان تکمیل','1 تا 3 روز'],['میزان ریزش','به دلیل واقعی بودن ممبرها، ریزش نامشخص است.'],['کیفیت سرویس','واقعی'],['فرمت لینک','لینک گروه بله']],{samples:['https://ble.ir/join/Arka_Member'],notes:[NOTES[2]]}),
    M('ممبر کانال بله {بدون ریزش 90 روز}',1280000,100,14000,[['زمان تکمیل','48 تا 72 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','90 روز بدون ریزش'],['لینک','لینک عمومی یا شناسه کانال']],{samples:['@Arka_Member','https://ble.ir/Arka_Member']}),
    M('ممبر کانال بله {بدون ریزش 12 ماه}',3190000,100,14000,[['زمان تکمیل','48 تا 72 ساعت'],['نوع ممبر','فیک'],['میزان ریزش','12 ماه بدون ریزش'],['لینک','لینک عمومی یا شناسه کانال']],{samples:['@Arka_Member','https://ble.ir/Arka_Member']})
   ]}]},
   {id:'rubika',n:'روبیکا',c:'#D9328E',d:'#A3166A',types:[]},
   {id:'eitaa',n:'ایتا',c:'#FF7634',d:'#C95A08',types:[]},
   {id:'tg',n:'تلگرام',c:'#2AABEE',d:'#1779B5',types:[]},
   {id:'ig',n:'اینستاگرام',c:'#E1306C',d:'#9B1F8F',types:[]},
   {id:'yt',n:'یوتیوب',c:'#F03A3A',d:'#B91C1C',types:[]},
  ];
}

/* ============ پایگاه داده (فعلاً در حافظهٔ همین مرورگر) ============ */
const newDB=()=>({v:3,users:{},data:{},orders:[],tickets:[],tid:0,oid:0,pays:[],payc:0,products:null,settings:{brand:'#6B4EE6',brand2:'#4B2FD0'}});
let DB=newDB(),me=null,st=null;
function loadDB(){
  if(window.__ARKA_STATE&&window.__ARKA_STATE.v===3){
    const d=window.__ARKA_STATE;d.pays=d.pays||[];d.payc=d.payc||0;d.tid=d.tid||0;return d;
  }
  return newDB();
}
function reloadDB(){/* state از سرور در boot و commit همگام است؛ برای تازه‌سازی */ if(window.__ARKA_STATE){const d=window.__ARKA_STATE;if(d&&d.v===3){DB=d;if(me&&DB.users[me.email]){const u=DB.users[me.email];if(st&&st.viewAs){me=Object.assign({},u);delete me.role}else me=u}}}}
const CAN=(()=>{try{localStorage.setItem('arka:t','1');localStorage.removeItem('arka:t');return true}catch(e){return false}})();
let commitSeq=0,commitPend=0;
async function freshCounters(){try{const r=await API.get('/api/state'),d=r&&r.db;if(d)['oid','payc','tid'].forEach(k=>{DB[k]=Math.max(DB[k]||0,d[k]||0)})}catch(e){}}
function commit(){
  window.__ARKA_STATE=DB;
  const seq=++commitSeq;commitPend++;
  API.post('/api/state',{db:DB}).then(r=>{
    commitPend--;
    if(!r||!r.adopt||!r.db||seq!==commitSeq)return;
    window.__ARKA_STATE=r.db;reloadDB();
    if(r.conflicts&&r.conflicts.length){const ms=r.conflict_msgs||[];toast((ms[0]||'هم‌زمان با تغییر دیگری ذخیره شد؛ اطلاعات تازه‌سازی شد')+(ms.length>1?' (و '+lkDigits(ms.length-1)+' مورد دیگر)':''),1);try{renderAll()}catch(e){}}
  }).catch(e=>{commitPend--;toast(e.message||'خطا در ذخیره',1)});
}
function pollBusy(){
  const a=document.activeElement;
  if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))return true;
  const sb=$('#sbg');if(sb&&sb.classList.contains('on'))return true;
  if(document.querySelector('.chat.on,#chat.on,.chatv.on'))return true;
  return commitPend>0;
}
async function syncPoll(){
  if(!me||!st||document.visibilityState!=='visible'||pollBusy())return;
  try{
    const r=await API.get('/api/state'),d=r&&r.db;
    if(d&&d.v===3&&(d.rev||0)>(DB.rev||0)&&!pollBusy()){window.__ARKA_STATE=d;reloadDB();renderAll()}
  }catch(e){}
}
setInterval(syncPoll,30000);
function mirrorMe(){const u=me&&DB.users[me.email];if(u&&u!==me){['first','last','avatar'].forEach(k=>{if(k in me)u[k]=me[k]})}}
const dd=em=>DB.data[em]||(DB.data[em]={bal:0,tx:[],notif:[]});
const prods=()=>{if(!DB.products)DB.products=seedProducts();return DB.products};
const PL=id=>prods().find(p=>p.id===id);
const ghost=id=>({id:id||'x',n:'—',c:'#64748B',d:'#334155'});
const isAdmin=()=>!!me&&me.role==='admin'&&!(st&&st.viewAs);
const uid=()=>Math.random().toString(36).slice(2,8)+Date.now().toString(36).slice(-3);

/* ============ رمز عبور امن ============ */
const hex=b=>[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const unhex=h=>new Uint8Array(h.match(/../g).map(x=>parseInt(x,16)));
const rndHex=()=>{const a=new Uint8Array(16);(window.crypto&&crypto.getRandomValues)?crypto.getRandomValues(a):a.forEach((_,i)=>a[i]=Math.random()*256);return hex(a)};
async function kdf(pw,salt,it){
  if(!(window.crypto&&crypto.subtle))return null;
  const k=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveBits']);
  return hex(await crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:unhex(salt),iterations:it},k,256));
}
async function verifyPw(u,em,pw){
  if(u.v===2){const h=await kdf(pw,u.salt,100000);return h!==null&&h===u.pass}
  if(u.pass===hash(em+':'+pw)){const salt=rndHex(),h=await kdf(pw,salt,100000);if(h){u.v=2;u.salt=salt;u.pass=h;commit()}return true}
  return false;
}
const LK=()=>{try{return JSON.parse(S.g('arka:lock')||'{}')}catch(e){return{}}};
function lockLeft(em){const r=LK()[em];return r&&r.until?Math.max(0,Math.ceil((r.until-Date.now())/1000)):0}
function failed(em){const L=LK(),r=L[em]||{n:0};r.n++;if(r.n>=5){r.until=Date.now()+(em===ADMIN_EMAIL?300000:60000);r.n=0}L[em]=r;S.s('arka:lock',JSON.stringify(L))}
function clearFails(em){const L=LK();delete L[em];S.s('arka:lock',JSON.stringify(L))}

/* ============ آیکن‌ها ============ */
const I={
 home:'<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 box:'<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
 wallet:'<path d="M3 7a2 2 0 0 1 2-2h13v4"/><path d="M3 7v10a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2z"/><path d="M16 14h2"/>',
 user:'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 lock:'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 eye:'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 eyeoff:'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/><path d="M3 3l18 18"/>',
 bell:'<path d="M6 9a6 6 0 0 1 12 0c0 6 2 7 2 7H4s2-1 2-7"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 back:'<path d="M9 6l6 6-6 6"/>',chev:'<path d="M15 6l-6 6 6 6"/>',
 repeat:'<path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5M21 12a9 9 0 0 1-15 6.7L3 16M3 21v-5h5"/>',
 head:'<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><path d="M4 14h3v5H5a1 1 0 0 1-1-1zM20 14h-3v5h2a1 1 0 0 0 1-1z"/>',
 bolt:'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 moon:'<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/>',
 sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
 camera:'<path d="M4 8a2 2 0 0 1 2-2h2l1.5-2h5L16 6h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><circle cx="12" cy="12.5" r="3.5"/>',
 mail:'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7.5 12 13l8.5-5.5"/>',
 lock:'<rect x="4.5" y="10.5" width="15" height="10" rx="3"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
 clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 drop:'<path d="M12 3s6 6.2 6 10.5A6 6 0 0 1 6 13.5C6 9.2 12 3 12 3z"/>',
 logout:'<path d="M9 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h4M16 8l4 4-4 4M20 12H9"/>',
 edit:'<path d="M4 20h4L19 9l-4-4L4 16z"/>',
 users:'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.8"/><path d="M17 14.5a5.5 5.5 0 0 1 4.5 5.5"/>',
 link:'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 flag:'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 shield:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
 warn:'<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
 send:'<path d="M3 11 21 4l-7 17-3-7z"/>',
 plus:'<path d="M12 5v14M5 12h14"/>',
 minus:'<path d="M5 12h14"/>',
 copy:'<rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/>',
 upload:'<path d="M12 16V4M7 9l5-5 5 5M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>',
 trash:'<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
 x:'<path d="M6 6l12 12M18 6 6 18"/>',
 check:'<path d="M5 12.5l4.5 4.5L19 7"/>',
 search:'<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
 sliders:'<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
 palette:'<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 1.4-2-.6-1 0-2.2 1.3-2.2H17a4 4 0 0 0 4-4C21 6.5 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7" r="1"/>',
 chart:'<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
 ticket:'<path d="M3 9a2 2 0 0 0 0 6v3a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-3a2 2 0 0 1 0-6V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1z"/><path d="M14 5v14" stroke-dasharray="2 3"/>'
};
const ic=(n,s=22,w=2)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${I[n]||''}</svg>`;
const coin=s=>`<svg viewBox="0 0 64 64" width="${s}" height="${s}" aria-hidden="true"><use href="#coin"/></svg>`;
const okc=c=>/^#[0-9a-f]{6}$/i.test(c||'');
const sc=(c,f='#64748B')=>okc(c)?c:f;
const logo=(p,s)=>p.img?`<img class="logo-img" src="${esc(p.img)}" width="${s}" height="${s}" alt="${esc(p.n)}">`:
  SYMS.includes(p.id)?`<svg class="logo" width="${s}" height="${s}" viewBox="0 0 48 48" role="img" aria-label="${esc(p.n)}"><use href="#lg-${p.id}"/></svg>`:
  `<span class="lgf" style="width:${s}px;height:${s}px;font-size:${Math.round(s*.46)}px;--c1:${sc(p.c)};--c2:${sc(p.d)}">${esc((p.n||'?').trim().charAt(0))}</span>`;
const DEF='data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9B86FF"/><stop offset="1" stop-color="#4B2FD0"/></linearGradient></defs><rect width="96" height="96" fill="url(#g)"/><circle cx="48" cy="38" r="17" fill="#fff" fill-opacity=".92"/><path d="M14 96c2-22 16-34 34-34s32 12 34 34z" fill="#fff" fill-opacity=".92"/></svg>');

/* ============ ابزارها ============ */
const $=s=>document.querySelector(s);
const fa=n=>Math.round(+n||0).toLocaleString('fa-IR');
const fd=s=>String(s).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
const num=s=>+String(s).replace(/[۰-۹]/g,d=>'۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g,d=>'٠١٢٣٤٥٦٧٨٩'.indexOf(d)).replace(/[,٬\s]/g,'')||0;
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cleanTitle=s=>String(s).replace(/[{}]/g,'');
const hhmm=ts=>new Date(ts).toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit'});
const fmt=ts=>new Date(ts).toLocaleDateString('fa-IR')+' • '+hhmm(ts);
const jdate=ts=>new Date(ts||Date.now()).toLocaleDateString('fa-IR',{day:'numeric',month:'long',year:'numeric'});
function ago(ts){const s=Math.floor((Date.now()-ts)/1000);if(s<60)return'همین حالا';if(s<3600)return fa(s/60|0)+' دقیقه پیش';if(s<86400)return fa(s/3600|0)+' ساعت پیش';return fa(s/86400|0)+' روز پیش'}
const buzz=()=>navigator.vibrate&&navigator.vibrate(14);
const fullOf=u=>u?`${u.first} ${u.last}`.trim():'کاربر حذف‌شده';
const full=()=>fullOf(me);
const avSrc=u=>u&&u.avatar?u.avatar:DEF;
const avImg=u=>`<img class="avimg" src="${esc(avSrc(u===undefined?me:u))}" alt="">`;
const lat=s=>String(s).replace(/[۰-۹]/g,d=>'۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g,d=>'٠١٢٣٤٥٦٧٨٩'.indexOf(d));
const paidOrder=o=>!o.pay||((DB.pays.find(p=>p.id===o.pay)||{}).s==='ok');
const spentOf=em=>DB.orders.filter(o=>o.u===em&&paidOrder(o)).reduce((a,o)=>a+o.price-(o.rf||0),0);
const pct=o=>o.qty?Math.min(100,Math.round(o.dn/o.qty*100)):0;
function shade(hex6,f){const n=parseInt(hex6.slice(1),16);let r=n>>16,g=n>>8&255,b=n&255;const t=f<0?0:255,p=Math.abs(f);r=Math.round((t-r)*p+r);g=Math.round((t-g)*p+g);b=Math.round((t-b)*p+b);return'#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1)}
function toast(t){const e=$('#toast');e.textContent=t;e.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(()=>e.classList.remove('on'),2600);buzz()}
function notifyUser(em,t){dd(em).notif.unshift({t,ts:Date.now(),r:1});commit()}
const notify=t=>notifyUser(me.email,t);

/* ============ تم و رنگ برند ============ */
const isDark=()=>{const r=document.documentElement;return r.dataset.mode==='dark'||(r.dataset.mode==='auto'&&matchMedia('(prefers-color-scheme: dark)').matches)};
function syncTheme(anim){
  document.querySelectorAll('.themeIc').forEach(e=>{e.innerHTML=ic(isDark()?'sun':'moon',22);if(anim&&e.firstElementChild)e.firstElementChild.classList.add('pop')});
  $('#tcMeta').content=isDark()?'#0E0B22':sc(DB.settings.brand,'#6B4EE6');
}
function toggleTheme(){const m=isDark()?'light':'dark';document.documentElement.dataset.mode=m;S.s('arka:theme',m);syncTheme(true)}
function applyBrand(b,b2){const r=document.documentElement.style;r.setProperty('--brand',sc(b,'#6B4EE6'));r.setProperty('--brand2',sc(b2,'#4B2FD0'))}
const savedTheme=S.g('arka:theme');if(savedTheme)document.documentElement.dataset.mode=savedTheme;
matchMedia('(prefers-color-scheme: dark)').addEventListener&&matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>syncTheme());

/* ============ تیکت‌ها: منطق ============ */
const activeCount=em=>DB.tickets.filter(t=>t.u===em&&t.s==='open').length;
function sweep(){
  let ch=false;
  DB.tickets.forEach(t=>{if(t.s==='open'&&Date.now()-t.up>AUTO){t.s='closed';t.auto=1;t.cl=Date.now();t.m.push({f:'s',t:'این تیکت به دلیل ۳ روز بدون گفت‌وگو به‌صورت خودکار بسته شد.',ts:Date.now()});dd(t.u).notif.unshift({t:`تیکت #${fa(t.id)} به‌صورت خودکار بسته شد`,ts:Date.now(),r:1});ch=true}});
  if(ch)commit();return ch;
}
function tkState(t,adm){
  if(t.s==='closed')return{k:'closed',n:t.auto?'بسته شد (خودکار)':'بسته شده',c:'#64748B',tc:'#FFFFFF'};
  return t.w==='a'?{k:'wait',n:adm?'نیازمند پاسخ':'در انتظار پاسخ',c:'#F59E0B',tc:'#2B1D00'}:{k:'ans',n:'پاسخ داده شد',c:'#16A34A',tc:'#FFFFFF'};
}
function closeIn(t){const ms=t.up+AUTO-Date.now();if(ms<=0)return'در حال بسته شدن';if(ms<DAY)return`بسته شدن خودکار: ${fa(Math.ceil(ms/36e5))} ساعت دیگر`;return`بسته شدن خودکار: ${fa(Math.ceil(ms/DAY))} روز دیگر`}
function tkCard(t,adm){
  const s=tkState(t,adm),owner=DB.users[t.u],last=[...t.m].reverse().find(x=>x.f!=='s'),unread=adm?t.ur&&t.ur.a:t.ur&&t.ur.u;
  const who=!last?'':last.f==='u'?(adm?'کاربر':'شما'):'پشتیبانی';
  return `<div class="pass" style="${stStyle(s)}" data-act="tk" data-id="${t.id}" role="button">
   <div class="pass-top"><span class="pass-lg">${ic('ticket',24)}</span><div class="pass-t"><b>تیکت #${fa(t.id)}</b><small>${esc(t.c)} • ${ago(t.up)}</small></div><span class="spill">${s.n}</span></div>
   <div class="pass-cut"></div>
   <div class="pass-body">
    ${adm?`<div class="pass-u"><img src="${esc(avSrc(owner))}" alt=""><span>${esc(fullOf(owner))}</span><small>${esc(t.u)}</small></div>`:''}
    <b class="pass-ti clamp">${esc(t.sub)}</b>
    ${last?`<div class="pv"><b>${who}:</b> ${esc(last.t.slice(0,120))}</div>`:''}
    <div class="pass-f"><span class="hint">${t.s==='open'?ic('clock',14)+closeIn(t):ic('lock',14)+(adm?'بسته شده':'بسته شده؛ برای موضوع جدید تیکت تازه ثبت کن')}</span>${unread?`<span class="newp">${adm?'پیام جدید':'پاسخ جدید'}</span>`:''}</div>
   </div></div>`;
}
function bub(m,adm){
  if(m.f==='s'){const tx=m.t==='__CLOSED_BY_USER__'?(adm?'تیکت توسط کاربر بسته شد.':'تیکت توسط شما بسته شد.'):m.t;return `<div class="sysm">${esc(tx)}</div>`;}
  const mine=adm?m.f==='a':m.f==='u';
  const act=(adm&&m.f==='a')?`<span class="mact"><button data-act="mged" data-ts="${m.ts}">ویرایش</button><button data-act="mgdl" data-ts="${m.ts}">حذف</button></span>`:'';
  return `<div class="bub ${mine?'me':'them'}">${esc(m.t)}<small>${hhmm(m.ts)}${m.ed?' • ویرایش‌شده':''}</small>${act}</div>`;
}
function openTicket(id){
  const t=DB.tickets.find(x=>x.id===id);if(!t)return;
  st.tkid=id;const v=isAdmin()?'a':'u';
  if(!t.ur)t.ur={u:0,a:0};
  t.ur[v]=0;
  // وقتی کاربر تیکت را می‌بیند، اعلان «پاسخ جدید» هم خوانده شود
  if(v==='u'){
    const d=dd(me.email);
    (d.notif||[]).forEach(n=>{
      if(n&&n.r&&typeof n.t==='string'&&(n.t.indexOf('تیکت #'+fa(t.id))>=0||n.t.indexOf('تیکت #'+t.id)>=0))n.r=0;
    });
  }
  commit();
  document.body.style.overflow='hidden';renderChat(true);chrome();
}
function closeChat(){st.tkid=null;$('#tkvin').innerHTML='';$('#tkv').classList.remove('on');document.body.style.overflow='';renderAll()}
function renderChat(scroll){
  const t=DB.tickets.find(x=>x.id===st.tkid),ov=$('#tkv');
  if(!t){ov.classList.remove('on');return}
  const adm=isAdmin(),owner=DB.users[t.u],s=tkState(t,adm),closed=t.s==='closed',draft=$('#tkI')?$('#tkI').value:'';
  const body=$('#tkB'),keep=body?body.scrollHeight-body.scrollTop-body.clientHeight<80:true;
  $('#tkvin').innerHTML=`
   <header class="tkv-h ${adm?'adm':''}">
    <button class="ib" data-act="tkback" aria-label="بازگشت">${ic('back')}</button>
    <div class="tt"><b>${esc(t.sub)}</b><small>تیکت #${fa(t.id)} • ${esc(t.c)}${adm?' • '+esc(fullOf(owner)):''}</small></div>
    ${adm?`<button class="ib" data-act="tkdel" aria-label="حذف تیکت">${ic('trash',20)}</button>`:''}${(closed&&!adm)?'':`<button class="ib" data-act="${closed?'tkopen':'tkclose'}" aria-label="${closed?'باز کردن مجدد':'بستن تیکت'}">${ic(closed?'repeat':'lock')}</button>`}
   </header>
   <div class="tkv-meta"><span class="spill2" style="${stStyle(s)}">${s.n}</span>${!closed?`<span class="cx">${ic('clock',14)}${closeIn(t)}</span>`:''}
    ${adm?`<button class="cx" data-act="uview" data-e="${esc(t.u)}">${ic('user',14)}مدیریت کاربر</button><span class="cx">${ic('wallet',14)}${fa(dd(t.u).bal)} تومان</span>`:''}</div>
   <div class="tkv-body" id="tkB">${t.m.map(m=>bub(m,adm)).join('')}</div>
   ${closed?`<div class="tkv-closed">${ic('info',16)}<span>${adm?'این تیکت بسته است؛ با ارسال پیام یا دکمهٔ باز کردن دوباره باز می‌شود.':'این تیکت بسته شده و دیگر باز نمی‌شود؛ برای موضوع جدید تیکت تازه ثبت کن.'}</span></div>`:''}
   <div class="tkv-bar" ${(closed&&!adm)?'style="display:none"':''}>${adm?`<div class="qr">${QR.map((q,i)=>`<button data-act="qr" data-i="${i}">${esc(q.s)}</button>`).join('')}</div>`:''}
    <div class="tkv-row"><textarea id="tkI" class="inp" rows="1" placeholder="پیامت را بنویس...">${esc(draft)}</textarea><button class="send" data-act="tksend" aria-label="ارسال">${ic('send',22)}</button></div></div>`;
  ov.classList.add('on');
  const b=$('#tkB');if(scroll||keep)b.scrollTop=b.scrollHeight;
  const ta=$('#tkI');ta.style.height='48px';ta.style.height=Math.min(130,ta.scrollHeight)+'px';
}
function sendTk(){
  const t=DB.tickets.find(x=>x.id===st.tkid);if(!t)return;
  const inp=$('#tkI'),txt=inp.value.trim();if(!txt)return;
  const adm=isAdmin(),ts=Date.now();
  if(t.s==='closed'){
    if(!adm){toast('این تیکت بسته شده است؛ تیکت جدید ثبت کن');return}
    if(activeCount(t.u)<MAXACT){t.s='open';t.auto=0;t.m.push({f:'s',t:'تیکت دوباره باز شد.',ts})}
  }
  t.m.push(adm?{f:'a',t:txt,ts,by:me.email}:{f:'u',t:txt,ts});t.up=ts;t.w=adm?'u':'a';t.ur=adm?{u:1,a:0}:{u:0,a:1};
  if(adm)notifyUser(t.u,`پاسخ جدید برای تیکت #${fa(t.id)}`);
  commit();inp.value='';renderChat(true);
}
function closeTk(id,by){
  const t=DB.tickets.find(x=>x.id===id);if(!t||t.s==='closed')return;
  t.s='closed';t.auto=0;t.cl=Date.now();t.m.push({f:'s',t:by==='a'?'تیکت توسط پشتیبانی بسته شد.':'__CLOSED_BY_USER__',ts:Date.now()});
  if(by==='a')notifyUser(t.u,`تیکت #${fa(t.id)} بسته شد`);
  commit();
}
function reopenTk(id){
  const t=DB.tickets.find(x=>x.id===id);if(!t)return;
  if(!isAdmin()){toast('تیکت بسته‌شده دوباره باز نمی‌شود؛ تیکت جدید ثبت کن');return}
  if(!isAdmin()&&activeCount(t.u)>=MAXACT){toast('حداکثر ۲ تیکت فعال داری؛ اول یکی را ببند');return}
  if(isAdmin()&&activeCount(t.u)>=MAXACT){toast('این کاربر ۲ تیکت فعال دارد');return}
  t.s='open';t.auto=0;t.up=Date.now();t.m.push({f:'s',t:'تیکت دوباره باز شد.',ts:Date.now()});commit();
}
function openNewTk(pre){
  pre=pre||{};
  const act=DB.tickets.filter(t=>t.u===me.email&&t.s==='open');
  if(act.length>=MAXACT){
    sheet(`<div class="sh">به سقف تیکت فعال رسیدی</div><div class="shp">حداکثر ${fa(MAXACT)} تیکت فعال می‌توانی داشته باشی. برای ثبت تیکت جدید، یکی از تیکت‌های زیر را ببند.</div>
     ${act.map(t=>`<div class="tkrow"><span class="t">#${fa(t.id)} — ${esc(t.sub)}</span><button data-act="tkclose2" data-id="${t.id}">بستن</button></div>`).join('')}`);
    return;
  }
  st.nt={c:pre.c||TK_CATS[0]};
  sheet(`<div class="sh">تیکت جدید</div><div class="shp">${fa(act.length)} از ${fa(MAXACT)} تیکت فعال</div>
   <div class="lbl">موضوع</div><div class="catc" id="nCats">${TK_CATS.map(c=>`<button data-act="nc" data-c="${c}" aria-pressed="${c===st.nt.c}">${c}</button>`).join('')}</div>
   <div class="lbl">عنوان</div><input class="inp" id="nS" maxlength="80" placeholder="مثلاً: سفارشم شروع نشده" value="${esc(pre.s||'')}">
   <div class="lbl">پیام</div><textarea class="inp" id="nM" placeholder="توضیح بده تا سریع‌تر کمکت کنیم..." style="--tc:var(--brand)">${esc(pre.m||'')}</textarea>
   <div class="err" id="nE"></div><button class="btn brand full" data-act="tkcreate">${ic('send',20)} ثبت تیکت</button>`);
}
async function createTk(){
  await freshCounters();
  const sub=$('#nS').value.trim(),msg=$('#nM').value.trim(),e=$('#nE');
  if(sub.length<3){e.textContent='عنوان تیکت را بنویس.';return}
  if(msg.length<3){e.textContent='پیامت را بنویس.';return}
  if(activeCount(me.email)>=MAXACT){e.textContent='به سقف تیکت فعال رسیدی.';return}
  const ts=Date.now();DB.tid++;
  DB.tickets.unshift({id:DB.tid,u:me.email,c:st.nt.c,sub,s:'open',w:'a',ts,up:ts,m:[{f:'u',t:msg,ts}],ur:{u:0,a:1}});
  commit();closeSheet();toast('تیکت ثبت شد');renderAll();openTicket(DB.tid);
}

/* ============ ابزارهای مدیر: اعلان، تیکت، بکاپ ============ */
function annSend(){
  if(!isAdmin())return;
  const s=($('#anM').value||'').trim(),to=$('#anT').value,e=$('#anE');
  if(s.length<2){e.textContent='متن اعلان را بنویس.';return}
  const L=to==='*'?Object.values(DB.users).filter(u=>u.role!=='admin').map(u=>u.email):[to];
  if(!L.length){e.textContent='کاربری برای ارسال وجود ندارد.';return}
  const ts=Date.now();
  L.forEach(em=>{if(!DB.users[em])return;const d=dd(em);if(!Array.isArray(d.notif))d.notif=[];d.notif.unshift({t:s,ts,r:1})});
  commit();$('#anM').value='';e.textContent='';toast('اعلان برای '+fa(L.length)+' کاربر ارسال شد');
}
function msgEdit(ts){
  const t=DB.tickets.find(x=>x.id===st.tkid);const m=t&&t.m.find(x=>String(x.ts)===String(ts)&&x.f==='a');if(!m)return;
  const v=prompt('ویرایش پیام:',m.t);if(v===null)return;const x=v.trim();if(!x)return;
  m.t=x;m.ed=Date.now();commit();renderChat();
}
function msgDel(ts){
  const t=DB.tickets.find(x=>x.id===st.tkid);const m=t&&t.m.find(x=>String(x.ts)===String(ts)&&x.f==='a');if(!m)return;
  if(!confirm('این پیام حذف شود؟'))return;
  t.m=t.m.filter(x=>x!==m);commit();renderChat();
}
function tkDelete(){
  const t=DB.tickets.find(x=>x.id===st.tkid);if(!t||!isAdmin())return;
  if(!confirm('کل این تیکت برای همیشه حذف شود؟'))return;
  DB.tickets=DB.tickets.filter(x=>x.id!==t.id);commit();closeChat();toast('تیکت حذف شد');
}
async function bkAuth(){
  const opt=await API.post('/api/backup/options',{});
  if(opt.mode==='webauthn'){
    if(!window.PublicKeyCredential)throw new Error('اثر انگشت در این مرورگر پشتیبانی نمی‌شود');
    const cred=await navigator.credentials.get({publicKey:{challenge:u8(opt.challenge),timeout:opt.timeout||120000,rpId:opt.rpId,
      allowCredentials:(opt.allowCredentials||[]).map(c=>({type:'public-key',id:u8(c.id)})),userVerification:'required'}});
    return {cid:opt.cid,id:b64u(cred.rawId),clientDataJSON:b64u(cred.response.clientDataJSON),authenticatorData:b64u(cred.response.authenticatorData),signature:b64u(cred.response.signature)};
  }
  const pw=prompt('رمز عبور مدیر را وارد کنید:');if(!pw)throw new Error('لغو شد');
  return {password:pw};
}
function bkPost(path,body){
  return fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Device':deviceId(),'X-Token':(S.g('arka:token')||''),'X-CSRF':(window.__CSRF||'')},body:JSON.stringify(body)});
}
async function bkDownload(bid){
  try{
    toast('در حال تأیید هویت…');const a=await bkAuth();toast('در حال ساخت بکاپ…');
    const r=await bkPost('/api/backup/download',Object.assign({bid:bid||0},a));
    if(!r.ok){let d={};try{d=await r.json()}catch(e){}toast(d.detail||('خطا '+r.status),1);return}
    const blob=await r.blob(),m=/filename="?([^";]+)"?/.exec(r.headers.get('Content-Disposition')||'');
    const el=document.createElement('a');el.href=URL.createObjectURL(blob);el.download=m?m[1]:'arka-backup.sql';
    document.body.appendChild(el);el.click();el.remove();setTimeout(()=>URL.revokeObjectURL(el.href),4000);toast('بکاپ دانلود شد');
  }catch(e){toast(e.message||'خطا در بکاپ',1)}
}
function bufB64(buf){const a=new Uint8Array(buf);let s='';for(let i=0;i<a.length;i+=0x8000)s+=String.fromCharCode.apply(null,a.subarray(i,i+0x8000));return btoa(s)}
async function bkRestore(file,bid){
  try{
    if(!confirm('همهٔ اطلاعات فعلی سایت با محتوای این بکاپ جایگزین می‌شود (از وضعیت فعلی هم یک نسخهٔ امن گرفته می‌شود). ادامه؟'))return;
    let body={bid:bid||0};
    if(file){if(file.size>18*1024*1024){toast('فایل بیشتر از ۱۸ مگابایت است',1);return}toast('در حال خواندن فایل…');body.file=bufB64(await file.arrayBuffer())}
    toast('در حال تأیید هویت…');const a=await bkAuth();toast('در حال بازیابی…');
    const r=await bkPost('/api/backup/restore',Object.assign(body,a));
    const d=await r.json().catch(()=>({}));
    if(!r.ok){toast(d.detail||('خطا '+r.status),1);return}
    toast(`بازیابی شد: ${fa(d.users)} کاربر، ${fa(d.orders)} سفارش`);setTimeout(()=>location.reload(),1500);
  }catch(e){toast(e.message||'خطا در بازیابی',1)}
}
function bkPick(){
  const i=document.createElement('input');i.type='file';i.accept='.sql,.dump,.backup,.gz,.txt,application/octet-stream';
  i.onchange=()=>{const f=i.files&&i.files[0];if(f)bkRestore(f,0)};i.click();
}
async function bkList(){
  try{
    const r=await API.post('/api/backup/list',{});
    const rows=(r.items||[]).map(x=>`<div class="bkrow"><div class="t">${fmt(x.ts*1000)}<br><small>${esc(x.label||'')} • ${fa(Math.round(x.size/1024))} کیلوبایت</small></div><button data-act="bkdl" data-id="${x.id}">دانلود</button><button data-act="bkrs" data-id="${x.id}">بازگردانی</button></div>`).join('');
    sheet(`<div class="sh">نسخه‌های خودکار سایت</div><div class="shp">هر ${fa(r.hours)} ساعت یک نسخه داخل خود سایت ذخیره می‌شود (آخرین ${fa(r.keep)} نسخه).</div>${rows||'<div class="pv" style="text-align:center;margin:14px 0">هنوز نسخه‌ای ذخیره نشده.</div>'}`);
  }catch(e){toast(e.message||'خطا',1)}
}

/* ============ chrome ============ */
const NAV=[['home','home','خانه'],['orders','box','سفارش‌ها'],['tickets','ticket','تیکت‌ها'],['wallet','wallet','کیف پول'],['me','user','حساب']];
const ANAV=[['a-dash','chart','داشبورد'],['a-orders','box','سفارش‌ها'],['a-pays','wallet','پرداخت‌ها'],['a-tickets','ticket','تیکت‌ها'],['a-users','users','کاربران'],['a-manage','sliders','مدیریت']];
function badgeFor(k){
  if(!me)return 0;
  if(isAdmin()){if(k==='a-tickets')return DB.tickets.filter(t=>t.s==='open'&&t.w==='a').length;if(k==='a-orders')return DB.orders.filter(o=>o.st==='queue').length;if(k==='a-pays')return DB.pays.filter(p=>p.s==='pending').length;return 0}
  if(k==='tickets')return DB.tickets.filter(t=>t.u===me.email&&t.ur&&t.ur.u).length;
  return 0;
}
function chrome(){
  if(!st||!me)return;
  const items=isAdmin()?ANAV:NAV,un=isAdmin()?0:dd(me.email).notif.filter(n=>n.r).length;
  $('#nav').classList.toggle('six',items.length>5);
  $('#nav').innerHTML=items.map(([k,i,n])=>{const b=badgeFor(k);return `<button data-act="nav" data-to="${k}" class="${(st.view===k||(k==='home'&&st.view==='plat'))?'on':''}" aria-label="${n}">${ic(i,22)}<span>${n}</span>${b?`<span class="badge">${fa(b)}</span>`:''}</button>`}).join('');
  document.querySelectorAll('.bellDot').forEach(e=>e.classList.toggle('on',un>0));
}

/* ============ خانه (کاربر) ============ */
const arch=(w,s)=>`<svg width="${s}" height="${s}" viewBox="0 0 48 48" aria-hidden="true"><path d="M8 42V22a16 16 0 0 1 32 0v20" fill="none" stroke="#fff" stroke-width="${w}" stroke-linecap="round"/><path d="M17 42V24a7 7 0 0 1 14 0v18" fill="none" stroke="#FFC83A" stroke-width="${w*.8}" stroke-linecap="round"/></svg>`;
function memberCard(){
  const bal=dd(me.email).bal;
  return `<div class="mc" role="button" tabindex="0" aria-label="کارت عضویت — برای دیدن موجودی لمس کنید" data-act="flipcard"><div class="mc-t">
    <div class="mc-face">
      <span class="mc-wm">${arch(3,200)}</span>
      <div class="mc-r1"><div class="mc-brand">${arch(5,24)}ARKA</div>${coin(34)}</div>
      <svg class="mc-chip" width="44" height="32" viewBox="0 0 38 28" aria-hidden="true"><rect width="38" height="28" rx="6" fill="url(#cFace)"/><path d="M0 10h38M0 18h38M13 0v28M25 0v28" stroke="#a85900" stroke-opacity=".35" fill="none"/></svg>
      <div class="mc-r3"><div class="mc-n"><small>نام و نام خانوادگی</small><b>${esc(full())}</b></div><div class="mc-d"><small>تاریخ عضویت</small><b>${jdate(me.joined)}</b></div></div>
    </div>
    <div class="mc-back">
      <span class="mc-wm">${arch(3,200)}</span>
      <div class="mc-r1"><div class="mc-brand">${arch(5,24)}ARKA</div><span style="font-size:11px;opacity:.6;font-weight:700">BALANCE</span></div>
      <div>
        <div class="bal-lab">موجودی کیف پول</div>
        <div class="bal-val">${fa(bal)}<span>تومان</span></div>
      </div>
      <div class="hint">برای بازگشت دوباره لمس کنید</div>
    </div>
  </div></div>`;
}
function renderHome(){
  const tb=badgeFor('tickets');
  $('#v-home').innerHTML=`
  <header class="top"><div class="row">
    <button class="avatar" data-act="profile" aria-label="پروفایل">${avImg()}</button>
    <div class="who"><b>${esc(full())}</b></div>
    <button class="ib themeIc" data-act="theme" aria-label="تغییر تم"></button>
    <button class="ib" data-act="bell" aria-label="اعلان‌ها">${ic('bell')}<i class="bellDot"></i></button>
  </div></header>
  <section class="balance"><div class="coinw">${coin(68)}</div>
    <div class="m"><small>موجودی کیف پول</small><strong>${fa(dd(me.email).bal)}</strong><span class="unit">تومان</span></div>
    <button class="mini" data-act="nav" data-to="wallet">شارژ</button></section>
  ${memberCard()}
  ${fpHomeCard()}
  <h2 class="sec">انتخاب اپلیکیشن</h2>
  <div class="grid stg">${prods().map(p=>`<button class="tile" style="--tc:${sc(p.c)}" data-act="plat" data-id="${esc(p.id)}">${logo(p,64)}<h3>${esc(p.n)}</h3></button>`).join('')}</div>
  <h2 class="sec">میانبرها</h2>
  <div class="list">
    <button class="lr" data-act="nav" data-to="tickets" style="--tc:#14B27F"><div class="ico">${ic('head')}</div><div class="t"><b>پشتیبانی و تیکت‌ها</b><span class="s">سوالی داری؟ تیکت بده</span></div>${tb?`<span class="badge">${fa(tb)}</span>`:''}<span class="ch">${ic('chev',20)}</span></button>
    <a class="lr" href="${BALE.url}" target="_blank" rel="noopener"><div class="ico" style="background:none">${logo({id:'bale',n:'بله'},44)}</div><div class="t"><b>کانال بله آرکا</b><span class="s" style="display:block;direction:ltr;text-align:right">${BALE.id}</span></div><span class="ch">${ic('chev',20)}</span></a>
  </div>`;
}

/* ============ صفحه اپلیکیشن ============ */
function openPlat(pid){st.pid=pid;st.oc=null;nav('plat')}
function renderPlat(){
  if(!st.pid){$('#v-plat').innerHTML='';return}
  const p=PL(st.pid);if(!p){st.pid=null;$('#v-plat').innerHTML='';return}
  const cats=p.types.filter(t=>t.items.length),c1=sc(p.c),c2=sc(p.d);
  const head=`<header class="top pgh" style="--tc:${c1};--tc2:${c2}"><div class="ph">
    <button class="ib" data-act="nav" data-to="home" aria-label="بازگشت" style="margin:0">${ic('back')}</button>
    <div class="tt"><b>${esc(p.n)}</b></div>${logo(p,56)}</div></header>`;
  if(!cats.length){$('#v-plat').innerHTML=head+`<div class="nop" style="--tc:${c1}">${logo(p,76)}<h3>فعلا محصولی نیست</h3><p>سرویس‌های ${esc(p.n)} به‌زودی اضافه می‌شود.</p></div>`;return}
  $('#v-plat').innerHTML=head+`<div class="cats stg" style="--tc:${c1};--tc2:${c2}">${cats.map(t=>`
   <div class="cat ${st.oc===t.id?'open':''}">
    <button class="cat-h" data-act="cat" data-id="${esc(t.id)}" aria-expanded="${st.oc===t.id}"><span class="cat-ic">${ic('users',26)}</span><span class="cat-t"><b>${esc(t.n)}</b><small>${fa(t.items.length)} سرویس</small></span><span class="cat-ch">${ic('chev',18,2.6)}</span></button>
    <div class="cat-b"><div class="cat-bi"><div class="cat-list">${t.items.map(it=>`
     <button class="pc" data-act="prod" data-t="${esc(t.id)}" data-i="${esc(it.id)}"><div class="pc-h"><b>${esc(fd(cleanTitle(it.n)))}</b><span class="pc-go">${ic('chev',16,2.8)}</span></div>
      <div class="pc-s"><div><small>حداقل</small><b>${fa(it.min)}</b></div><div><small>حداکثر</small><b>${fa(it.max)}</b></div><div class="pr"><small>هر ۱۰۰۰ عدد</small><b>${fa(it.rate)}</b></div></div></button>`).join('')}</div></div></div></div>`).join('')}</div>`;
}

/* ============ ثبت سفارش ============ */
function findItem(pid,tid,iid){const p=PL(pid),t=p&&p.types.find(x=>x.id===tid),it=t&&t.items.find(x=>x.id===iid);return it?{p,t,it}:null}
function openProd(tid,iid,keep){
  const f=findItem(st.pid,tid,iid);if(!f){toast('این سرویس دیگر موجود نیست');return}
  st.o=keep||{pid:f.p.id,tid,iid,link:'',qty:f.it.min};
  renderProd();
}
const SPI={'زمان شروع':'clock','زمان تکمیل':'flag','نوع ممبر':'user','میزان ریزش':'drop','کیفیت سرویس':'shield','لینک':'link','فرمت لینک':'link'};
function renderProd(){
  const o=st.o,f=findItem(o.pid,o.tid,o.iid);if(!f)return;
  const{p,it}=f;
  sheet(`<div class="ps-scroll" style="--tc:${sc(p.c)};--tc2:${sc(p.d)}">
   <div class="ps-hero">${logo(p,56)}<h3>${esc(fd(cleanTitle(it.n)))}</h3></div>
   <div class="ps-st"><div><small>حداقل</small><b>${fa(it.min)}</b></div><div><small>حداکثر</small><b>${fa(it.max)}</b></div><div class="pr"><small>هر ۱۰۰۰ عدد</small><b>${fa(it.rate)}</b></div></div>
   ${it.rows.length?`<div class="sec2">${ic('info',18)}مشخصات سرویس</div>
   <div class="specs">${it.rows.map(r=>`<div class="sp ${String(r[1]).length>24||/لینک/.test(r[0])?'w':''}"><span class="i">${ic(SPI[r[0]]||'info',18)}</span><div><small>${esc(r[0])}</small><b>${esc(fd(r[1]))}</b></div></div>`).join('')}</div>`:''}
   ${it.notes.length?`<div class="nt"><button class="nt-h" data-act="nt">${ic('warn',20)}<span style="flex:1;text-align:start">نکات مهم قبل از خرید</span>${ic('chev',16,2.6)}</button><div class="nt-b"><div class="nt-bi">${it.notes.map(n=>`<p>• ${esc(n)}</p>`).join('')}</div></div></div>`:''}
   <div class="sec2">${ic('link',18)}لینک و تعداد</div>
   <label class="fi"><span class="fic">${ic('link',19)}</span><input class="inp ltr" id="oL" placeholder="${esc(it.samples[0]||'')}" value="${esc(o.link)}" autocomplete="off" inputmode="url"></label>
   ${it.samples.length?`<div class="smp2"><span>نمونه لینک:</span>${it.samples.map(s=>`<button data-act="smp" data-v="${esc(s)}">${esc(s)}</button>`).join('')}</div>`:''}
   <div class="lbl"><span>تعداد دلخواه</span><em>از ${fa(it.min)} تا ${fa(it.max)}</em></div>
   <input class="inp" id="oQ" type="text" inputmode="numeric" value="${o.qty||''}" placeholder="مثلاً ${fa(it.min*2)}" autocomplete="off" style="text-align:center;font-weight:900;font-size:20px">
   <div class="pre" style="margin-top:8px"><button data-act="qset" data-v="${it.min}">حداقل (${fa(it.min)})</button><button data-act="qset" data-v="${it.max}">حداکثر (${fa(it.max)})</button></div>
  </div>
  <div class="buybar" style="--tc:${sc(p.c)}"><div class="err" id="oE"></div><div class="bb"><div class="tot"><small>مبلغ نهایی</small><div><b id="oT">—</b> <span>تومان</span></div></div><button class="btn brand" data-act="buy">${ic('bolt',20)} پرداخت از کیف پول</button></div>
   <button class="btn soft full sm" data-act="pfstart" style="margin-top:8px">${ic('wallet',18)} پرداخت مستقیم (کارت‌به‌کارت)</button></div>`,'ps');
  sumUpdate();
}
const price=(it,q)=>Math.max(100,Math.round(it.rate*q/1000));
function sumUpdate(){const t=$('#oT');if(!t||!st.o)return;const f=findItem(st.o.pid,st.o.tid,st.o.iid);if(!f)return;t.textContent=st.o.qty?fa(price(f.it,st.o.qty)):'—'}
async function buy(){
  await freshCounters();
  const o=st.o,f=findItem(o.pid,o.tid,o.iid),e=$('#oE');
  if(!f){e.textContent='این سرویس دیگر موجود نیست.';return}
  const{p,it}=f;
  if(o.link.trim().length<3){e.textContent='لینک را وارد کن.';return}
  if(!o.qty||o.qty<it.min||o.qty>it.max||o.qty!==Math.floor(o.qty)){e.textContent=`تعداد باید بین ${fa(it.min)} تا ${fa(it.max)} باشد.`;return}
  const total=price(it,o.qty),bal=dd(me.email).bal;
  if(total>bal){e.innerHTML=`موجودی کم است؛ ${fa(total-bal)} تومان کم داری. <a href="#" data-act="gocharge">شارژ کیف پول</a>`;return}
  DB.oid++;
  const ord={id:DB.oid,u:me.email,pid:p.id,tid:o.tid,iid:it.id,title:it.n,link:o.link.trim(),qty:o.qty,price:total,dn:0,st:'queue',ts:Date.now(),rf:0,note:''};
  DB.orders.unshift(ord);const d=dd(me.email);d.bal-=total;d.tx.unshift({t:`${p.n} — ${cleanTitle(it.n)}`,a:-total,ts:ord.ts});
  commit();notify(`سفارش #${fa(ord.id)} ثبت شد و در صف قرار گرفت`);
  closeSheet();confetti();toast('سفارش ثبت شد');nav('orders');
}

/* ============ سفارش‌ها (کارت) ============ */
const payOf=o=>o.pay?DB.pays.find(p=>p.id===o.pay):null;
const payPending=o=>{const p=payOf(o);return !!p&&p.s==='pending'};
const pendRow=o=>payPending(o)?`<div class="onote">${ic('clock',16)}<span>پرداخت مستقیم این سفارش در انتظار تایید پشتیبانی است.</span></div>`:'';
function orderCard(o,adm){
  const p=PL(o.pid)||ghost(o.pid),s=stMeta(o.st),pc=pct(o),owner=adm?DB.users[o.u]:null;
  return `<div class="pass ${s.wh?'wh':''}" style="${stStyle(s)};--tc:${sc(p.c)}">
   <div class="pass-top"><span class="pass-lg">${logo(p,38)}</span><div class="pass-t"><b>سفارش #${fa(o.id)}</b><small>${esc(p.n)} • ${fmt(o.ts)}</small></div><span class="spill">${s.n}</span></div>
   <div class="pass-cut"></div>
   <div class="pass-body">
    ${adm?`<div class="pass-u"><img src="${esc(avSrc(owner))}" alt=""><span>${esc(fullOf(owner))}</span><small>${esc(o.u)}</small></div>`:''}
    <b class="pass-ti clamp">${esc(fd(cleanTitle(o.title)))}</b>
    <div class="pg2"><span class="pg2-n">${fa(pc)}٪</span><div class="pbar"><i style="--p:${pc}%"></i></div></div>
    <div class="pg2-s">${fa(o.dn)} از ${fa(o.qty)} عدد انجام شده</div>
    <div class="ord-lk">${ic('link',15)}<span>${esc(o.link)}</span></div>
    ${o.note?`<div class="onote">${ic('info',16)}<span>${esc(o.note)}</span></div>`:''}
    ${pendRow(o)}
    ${o.rf?`<div class="onote rf">${ic('wallet',16)}<span>${fa(o.rf)} تومان به کیف پول برگشته است.</span></div>`:''}
    <div class="pass-f"><span>${fa(o.price)} <small>تومان</small></span></div>
    <div class="oa">${adm?`<button class="pri" data-act="oedit" data-id="${o.id}">${ic('edit',17)} مدیریت سفارش</button>${payPending(o)?`<button data-act="pay" data-id="${o.pay}">${ic('wallet',17)} بررسی پرداخت</button>`:`<button data-act="uview" data-e="${esc(o.u)}">${ic('user',17)} کاربر</button>`}`:
      `<button data-act="reorder" data-id="${o.id}">${ic('repeat',17)} سفارش مجدد</button><button data-act="tkorder" data-id="${o.id}">${ic('head',17)} تیکت برای سفارش</button>`}</div>
   </div></div>`;
}
function fbar(cnt,cur,act){return `<div class="fbar">${[ALL,...STS].map(s=>`<button class="fc ${s.wh?'wh':''}" style="${stStyle(s)}" data-act="${act}" data-id="${s.k}" aria-pressed="${cur===s.k}"><i class="dot"></i>${s.n}<b>${fa(cnt(s.k))}</b></button>`).join('')}</div>`}
function renderOrders(){
  const mine=DB.orders.filter(o=>o.u===me.email),cnt=k=>k==='all'?mine.length:mine.filter(o=>o.st===k).length;
  const f=st.tab==='all'?mine:mine.filter(o=>o.st===st.tab);
  $('#v-orders').innerHTML=`<header class="top pgh"><div class="ph"><div class="tt"><b>سفارش‌های من</b><small>پیگیری لحظه‌ای سفارش‌ها</small></div><div class="big">${ic('box',26)}</div></div></header>
  ${fbar(cnt,st.tab,'tab')}
  ${f.length?f.map(o=>orderCard(o,false)).join(''):`<div class="empty">${ic('box',44,1.5)}${mine.length?'سفارشی با این وضعیت نیست.':'هنوز سفارشی نداری.<br>یک اپلیکیشن را انتخاب کن و اولین سفارشت را بده.'}</div>`}`;
}

/* ============ تیکت‌ها (کاربر) ============ */
function renderTickets(){
  const mine=DB.tickets.filter(t=>t.u===me.email),act=mine.filter(t=>t.s==='open').length;
  const f=st.ttab==='open'?mine.filter(t=>t.s==='open'):st.ttab==='closed'?mine.filter(t=>t.s==='closed'):mine;
  const cnt=k=>k==='all'?mine.length:k==='open'?act:mine.length-act;
  $('#v-tickets').innerHTML=`<header class="top pgh"><div class="ph"><div class="tt"><b>پشتیبانی</b><small>تیکت‌هایت را اینجا ببین</small></div><div class="big">${ic('head',26)}</div></div></header>
  <section class="tkh"><div class="tkh-r"><div class="t"><b>${fa(act)} از ${fa(MAXACT)} تیکت فعال</b><div class="slots">${Array.from({length:MAXACT},(_,i)=>`<i class="${i<act?'on':''}"></i>`).join('')}</div></div></div>
   <button class="btn brand full" data-act="tknew">${ic('plus',20,2.6)} تیکت جدید</button></section>
  <div class="tkfb">${[['all','همه'],['open','باز'],['closed','بسته‌شده']].map(([k,n])=>`<button class="fc tkc" data-act="ttab" data-id="${k}" aria-pressed="${st.ttab===k}"><i class="dot"></i>${n}<b>${fa(cnt(k))}</b></button>`).join('')}</div>
  ${f.length?f.map(t=>tkCard(t,false)).join(''):`<div class="empty">${ic('ticket',44,1.5)}${mine.length?'تیکتی در این بخش نیست.':'هنوز تیکتی نداری.<br>هر سوالی داری با تیکت بپرس.'}</div>`}
  <p class="wnote" style="margin-top:16px">${ic('info',16)}<span>هر تیکت اگر ۳ روز بدون گفت‌وگو بماند، خودکار بسته می‌شود. تیکت بسته‌شده را هم می‌توانی با ارسال پیام دوباره باز کنی.</span></p>`;
}

/* ============ کیف پول ============ */
function renderWallet(){
  const d=dd(me.email),mp=DB.pays.filter(p=>p.u===me.email);
  $('#v-wallet').innerHTML=`<header class="top pgh"><div class="ph"><div class="tt"><b>کیف پول</b><small>موجودی و پرداخت‌ها</small></div><div class="big">${ic('wallet',26)}</div></div></header>
  <section class="balance"><div class="coinw">${coin(68)}</div><div class="m"><small>موجودی شما</small><strong>${fa(d.bal)}</strong><span class="unit">تومان</span></div></section>
  <section class="wcta"><div class="wc-h"><div><b>شارژ حساب</b><small>کارت‌به‌کارت • تایید توسط پشتیبانی</small></div><span class="rng">${fa(CH_MIN/1000)} هزار تا ${fa(CH_MAX/1e6)} میلیون تومان</span></div>
   <div class="wsteps">${[['wallet','مبلغ'],['copy','واریز'],['upload','ارسال فیش'],['shield','تایید']].map(([i,n],k)=>`${k?'<span class="wl"></span>':''}<div class="wst"><i>${ic(i,18)}</i>${n}</div>`).join('')}</div>
   <button class="btn wbtn" data-act="pfcharge">${ic('bolt',20)} شروع شارژ حساب</button></section>
  <h2 class="sec">پرداخت‌های من</h2>
  <div class="list">${mp.length?mp.map(p=>{const s=PAYST[p.s];return `<div class="tx"><div>${p.kind==='order'?`خرید مستقیم سفارش #${fa(p.oid)}`:'شارژ کیف پول'} — ${fa(p.amt)} تومان<small>${fmt(p.ts)}${p.s==='rejected'&&p.note?' • '+esc(p.note):''}${p.s==='ok'&&p.cr&&p.cr!==p.amt?' • مبلغ تاییدشده '+fa(p.cr):''}</small></div><span class="pstat" style="${stStyle(s)}">${s.n}</span></div>`}).join(''):'<div class="tx none">هنوز پرداختی ثبت نکرده‌ای.</div>'}</div>
  <h2 class="sec">تراکنش‌ها</h2>
  <div class="list">${d.tx.length?d.tx.map(x=>`<div class="tx"><div>${esc(x.t)}<small>${x.ts?fmt(x.ts):esc(x.d||'')}</small></div><span class="${x.a>0?'plus':'minus'}">${x.a>0?'+':'−'}${fa(Math.abs(x.a))}</span></div>`).join(''):'<div class="tx none">تراکنشی برای شما ثبت نشده است!</div>'}</div>`;
}

/* ============ حساب (کاربر) ============ */
function renderMe(){
  const mine=DB.orders.filter(o=>o.u===me.email),by=prods().map(p=>({p,v:mine.filter(o=>o.pid===p.id&&paidOrder(o)).reduce((a,o)=>a+o.price-(o.rf||0),0)})).filter(x=>x.v>0),mx=Math.max(1,...by.map(x=>x.v));
  if(me&&DB.users[me.email]){me.fp=DB.users[me.email].fp||'';me.fp_on=!!DB.users[me.email].fp_on}
  $('#v-me').innerHTML=`<header class="top pgh"><div class="ph"><div class="tt"><b>حساب من</b><small>پروفایل و تنظیمات</small></div><div class="big">${ic('user',26)}</div></div></header>
  <section class="prof"><div class="a"><button class="av" data-act="profile" aria-label="ویرایش پروفایل">${avImg()}<span class="cam">${ic('camera',14)}</span></button><div class="nm"><b>${esc(full())}</b><small>عضو از ${jdate(me.joined)}</small></div></div>
   <div class="pst"><div><b>${fa(mine.length)}</b><span>سفارش</span></div><div><b>${fa(mine.filter(o=>o.st==='done').length)}</b><span>کامل‌شده</span></div><div><b>${fa(spentOf(me.email))}</b><span>مجموع خرید (تومان)</span></div></div></section>
  <h2 class="sec">هزینه به تفکیک اپلیکیشن</h2>
  <div class="card">${by.length?`<div class="bars">${by.map(x=>`<div class="bar" style="--tc:${sc(x.p.c)}"><span>${esc(x.p.n)}</span><i><b style="width:${x.v/mx*100}%"></b></i><span>${fa(x.v)}</span></div>`).join('')}</div>`:'<div style="color:var(--muted);font-size:13px">بعد از اولین سفارش، نمودار هزینه‌ها اینجا ساخته می‌شود.</div>'}</div>
  <h2 class="sec">تنظیمات</h2>
  ${settingsList()}`;
}
function fpHomeCard(){
  if(!me)return '';
  if(me&&DB.users[me.email]){me.fp=DB.users[me.email].fp||'';me.fp_on=!!DB.users[me.email].fp_on}
  const on=!!(me.fp_on&&me.fp);
  const can=typeof fpSupported==='function'&&fpSupported();
  return `<div class="fp-home">
    <div class="fp-home-txt">
      <b>اثر انگشت</b>
      <span>برای ورود سریع با حسگر گوشی</span>
      <span>${on?'وضعیت: فعال':(can?'وضعیت: خاموش — برای فعال‌سازی روشن کن':'وضعیت: این مرورگر پشتیبانی نمی‌کند')}</span>
    </div>
    <label class="fp-switch" title="اثر انگشت">
      <input type="checkbox" id="fpHome" ${on?'checked':''} ${can?'':'disabled'}>
      <span class="fp-switch-ui"></span>
    </label>
  </div>`;
}

function settingsList(){
  return `<div class="list"><button class="lr" data-act="profile" style="--tc:#E1306C"><div class="ico">${ic('edit')}</div><div class="t"><b>ویرایش پروفایل</b><span class="s">نام و عکس</span></div><span class="ch">${ic('chev',20)}</span></button>
  <button class="lr" data-act="theme" style="--tc:#6B4EE6"><div class="ico">${ic('moon')}</div><div class="t"><b>تغییر تم</b><span class="s">روشن / تاریک</span></div><span class="ch">${ic('chev',20)}</span></button>
  <a class="lr" href="${BALE.url}" target="_blank" rel="noopener" style="--tc:#14B27F"><div class="ico" style="background:none">${logo({id:'bale',n:'بله'},44)}</div><div class="t"><b>کانال بله آرکا</b><span class="s" style="display:block;direction:ltr;text-align:right">${BALE.id}</span></div><span class="ch">${ic('chev',20)}</span></a>
  <button class="lr" data-act="logout" style="--tc:#E5476F"><div class="ico">${ic('lock')}</div><div class="t"><b>خروج از حساب</b><span class="s">خروج از این دستگاه</span></div><span class="ch">${ic('chev',20)}</span></button>
  <button class="lr" data-act="logout-all" style="--tc:#E5476F"><div class="ico">${ic('lock')}</div><div class="t"><b>خروج از همه دستگاه‌ها</b><span class="s">بستن همهٔ نشست‌های باز</span></div><span class="ch">${ic('chev',20)}</span></button>
  </div>`;
}

/* ============ پنل ادمین ============ */
function admHead(title,sub,icon,extra){return `<header class="top pgh adm"><div class="ph"><div class="tt"><b>${title}</b><small>${sub}</small>${extra||''}</div><div class="big">${ic(icon,26)}</div></div></header>`}
function renderADash(){
  const us=Object.values(DB.users).filter(u=>u.role!=='admin'),os=DB.orders,tk=DB.tickets;
  const pend=DB.pays.filter(p=>p.s==='pending'),waiting=tk.filter(t=>t.s==='open'&&t.w==='a'),act=os.filter(o=>['queue','proc','run'].includes(o.st));
  const rev=os.filter(paidOrder).reduce((a,o)=>a+o.price-(o.rf||0),0),bal=us.reduce((a,u)=>a+dd(u.email).bal,0),mx=Math.max(1,...STS.map(s=>os.filter(o=>o.st===s.k).length));
  $('#v-a-dash').innerHTML=`<header class="top pgh adm dashboard-head"><div class="ph"><div class="tt"><b>پنل مدیریت</b><small>${esc(full())}</small><span class="adm-b">${ic('shield',13,2.4)}ADMIN</span></div><button class="ib" data-act="backupdb" aria-label="بکاپ دیتابیس" title="دانلود بکاپ امن">${ic('box',22)}</button><button class="ib themeIc" data-act="theme" aria-label="تغییر تم" style="margin-inline-start:0"></button><div class="big">${ic('chart',26)}</div></div>
  <button type="button" class="hdr-userui" data-act="userui">صفحه کاربران</button></header>
  <div class="kpis stg">
   <button class="kpi" data-act="nav" data-to="a-pays" style="--k:#F59E0B"><span class="kpi-i">${ic('wallet',22)}</span><b>${fa(pend.length)}</b><small>پرداخت در انتظار</small></button>
   <button class="kpi" data-act="nav" data-to="a-tickets" style="--k:#F0456F"><span class="kpi-i">${ic('ticket',22)}</span><b>${fa(waiting.length)}</b><small>تیکت بی‌پاسخ</small></button>
   <button class="kpi" data-act="nav" data-to="a-orders" style="--k:#3B82F6"><span class="kpi-i">${ic('box',22)}</span><b>${fa(act.length)}</b><small>سفارش فعال</small></button>
   <button class="kpi" data-act="nav" data-to="a-users" style="--k:#6B4EE6"><span class="kpi-i">${ic('users',22)}</span><b>${fa(us.length)}</b><small>کاربر</small></button>
  </div>
  <div class="wnote" style="margin-top:12px">${ic('chart',16)}<span>فروش خالص: <b>${fa(rev)}</b> تومان</span></div>
  <div class="wnote" style="margin-top:8px">${ic('wallet',16)}<span>مجموع موجودی کاربران: <b>${fa(bal)}</b> تومان</span></div>
  <h2 class="sec">وضعیت سفارش‌ها</h2>
  <div class="card" style="padding:0"><div class="sbars">${STS.map(s=>{const n=os.filter(o=>o.st===s.k).length;return `<div class="sbr" style="${stStyle(s)}"><span><i class="dot"></i>${s.n}</span><div class="tr"><b style="width:${n/mx*100}%"></b></div><span>${fa(n)}</span></div>`}).join('')}</div></div>
  <h2 class="sec">نیازمند پاسخ</h2>
  ${waiting.length?waiting.slice(0,3).map(t=>tkCard(t,true)).join(''):`<div class="empty">${ic('check',40,1.5)}همهٔ تیکت‌ها پاسخ داده شده‌اند.</div>`}
  <h2 class="sec">سفارش‌های در صف</h2>
  <div class="list">${os.filter(o=>o.st==='queue').slice(0,5).map(o=>{const p=PL(o.pid)||ghost(o.pid),s=stMeta(o.st);return `<button class="cr" data-act="oedit" data-id="${o.id}"><span class="lg">${logo(p,38)}</span><div class="t"><b class="clamp" style="-webkit-line-clamp:1">${esc(fd(cleanTitle(o.title)))}</b><small>#${fa(o.id)} • ${esc(fullOf(DB.users[o.u]))}</small></div><span class="spill" style="${stStyle(s)}">${s.n}</span></button>`}).join('')||'<div class="tx none">سفارشی در صف نیست.</div>'}</div>`;
}
function renderAOrders(){
  let all=DB.orders;if(st.fu)all=all.filter(o=>o.u===st.fu);
  const cnt=k=>k==='all'?all.length:all.filter(o=>o.st===k).length,f=st.atab==='all'?all:all.filter(o=>o.st===st.atab);
  $('#v-a-orders').innerHTML=admHead('مدیریت سفارش‌ها',`${fa(all.length)} سفارش`,'box')+fbar(cnt,st.atab,'atab')+
   (st.fu?`<div class="tkfb"><button class="fc tkc" data-act="fuclr" aria-pressed="true"><i class="dot"></i>${esc(fullOf(DB.users[st.fu]))} ${ic('x',14,2.6)}</button></div>`:'')+
   (f.length?f.map(o=>orderCard(o,true)).join(''):`<div class="empty">${ic('box',44,1.5)}سفارشی با این وضعیت نیست.</div>`);
}
function renderATickets(){
  let all=DB.tickets;if(st.fu)all=all.filter(t=>t.u===st.fu);
  const key=t=>t.s==='closed'?'closed':t.w==='a'?'wait':'ans';
  const cnt=k=>k==='all'?all.length:all.filter(t=>key(t)===k).length,f=st.aktab==='all'?all:all.filter(t=>key(t)===st.aktab);
  $('#v-a-tickets').innerHTML=admHead('تیکت‌های کاربران',`${fa(cnt('wait'))} تیکت نیازمند پاسخ`,'ticket')+
   `<div class="fbar">${[['all','همه'],['wait','نیازمند پاسخ'],['ans','پاسخ داده شد'],['closed','بسته‌شده']].map(([k,n])=>`<button class="fc tkc" data-act="aktab" data-id="${k}" aria-pressed="${st.aktab===k}"><i class="dot"></i>${n}<b>${fa(cnt(k))}</b></button>`).join('')}</div>`+
   (st.fu?`<div class="tkfb"><button class="fc tkc" data-act="fuclr" aria-pressed="true"><i class="dot"></i>${esc(fullOf(DB.users[st.fu]))} ${ic('x',14,2.6)}</button></div>`:'')+
   (f.length?f.map(t=>tkCard(t,true)).join(''):`<div class="empty">${ic('ticket',44,1.5)}تیکتی در این بخش نیست.</div>`);
}
function userRow(u){const o=DB.orders.filter(x=>x.u===u.email).length;return `<button class="urow" data-act="uview" data-e="${esc(u.email)}"><img src="${esc(avSrc(u))}" alt=""><div class="t"><b>${esc(fullOf(u))}</b><small>عضو از ${jdate(u.joined)}</small></div><div class="bl">${fa(dd(u.email).bal)}<small> تومان</small><small style="display:block">${fa(o)} سفارش</small></div></button>`}
function usersHtml(){
  const q=(st.q||'').trim().toLowerCase();
  const L=Object.values(DB.users).filter(u=>u.role!=='admin').filter(u=>!q||fullOf(u).toLowerCase().includes(q));
  return L.length?L.map(userRow).join(''):`<div class="empty" style="margin:12px 0 0">${ic('users',44,1.5)}کاربری پیدا نشد.</div>`;
}
function renderAUsers(){
  $('#v-a-users').innerHTML=admHead('کاربران',`${fa(Object.values(DB.users).filter(u=>u.role!=='admin').length)} کاربر ثبت‌نام‌شده`,'users')+
   `<div class="sch"><label class="fi"><span class="fic">${ic('search',19)}</span><input class="inp" id="uQ" placeholder="جستجوی نام" value="${esc(st.q||'')}" autocomplete="off"></label></div><div class="ulist" id="uList">${usersHtml()}</div>`;
}
function renderAManage(){
  const b=DB.settings;
  $('#v-a-manage').innerHTML=admHead('مدیریت','محصولات، رنگ‌ها و تنظیمات','sliders')+
  `<h2 class="sec" style="margin-top:20px">ارسال اعلان به کاربران</h2>
  <div class="card"><div class="lbl" style="margin-top:0">گیرنده</div>
   <select class="inp" id="anT"><option value="*">همهٔ کاربران</option>${Object.values(DB.users).filter(u=>u.role!=='admin').map(u=>`<option value="${esc(u.email)}">${esc(fullOf(u))}</option>`).join('')}</select>
   <div class="lbl">متن اعلان</div><textarea class="inp" id="anM" maxlength="300" placeholder="متن اعلان..." style="--tc:var(--brand)"></textarea>
   <div class="err" id="anE"></div><button class="btn brand full sm" data-act="annsend" style="margin-top:10px">${ic('send',18)} ارسال اعلان</button></div>
  <h2 class="sec" style="margin-top:20px">پشتیبان‌گیری و بازیابی</h2>
  <div class="card"><div class="pv" style="margin-bottom:10px">بکاپ مستقل از Railway: فایل SQL (PostgreSQL) که می‌توانی دانلود کنی یا فایل pg_dump / بکاپ قبلی را بدهی تا همه‌چیز از آن بازیابی شود.</div>
   <button class="btn brand full sm" data-act="backupdb">دانلود بکاپ کامل</button>
   <button class="btn soft full sm" data-act="bkrestore" style="margin-top:8px">بازیابی از فایل بکاپ</button>
   <button class="btn soft full sm" data-act="bklist" style="margin-top:8px">نسخه‌های خودکار سایت</button></div>
  `+`<h2 class="sec" style="margin-top:20px">رنگ‌بندی برنامه</h2>
  <div class="card"><div class="swr">${BRANDS.map(([c1,c2])=>`<button class="sw ${b.brand.toLowerCase()===c1.toLowerCase()?'on':''}" style="background:linear-gradient(135deg,${c1},${c2})" data-act="brand" data-a="${c1}" data-b="${c2}" aria-label="${c1}"></button>`).join('')}</div>
   <div class="two" style="margin-top:14px"><div><div class="lbl" style="margin-top:0">رنگ اصلی</div><input type="color" class="clr" id="bC1" value="${sc(b.brand,'#6B4EE6')}"></div><div><div class="lbl" style="margin-top:0">رنگ دوم</div><input type="color" class="clr" id="bC2" value="${sc(b.brand2,'#4B2FD0')}"></div></div>
   <button class="btn brand full sm" data-act="brandsave" style="margin-top:14px">ذخیرهٔ رنگ‌ها برای همه</button></div>
  <div class="sec3"><h2>محصولات و اپلیکیشن‌ها</h2><button class="mini2 pri" data-act="appnew" aria-label="اپلیکیشن جدید">${ic('plus',20,2.6)}</button></div>
  ${prods().map(p=>`<div class="am ${st.am===p.id?'open':''}" style="--tc:${sc(p.c)}"><button class="am-h" data-act="amtog" data-id="${esc(p.id)}">${logo(p,42)}<div class="t"><b>${esc(p.n)}</b><small>${fa(p.types.reduce((a,t)=>a+t.items.length,0))} سرویس</small></div><span class="cd"><i style="background:${sc(p.c)}"></i><i style="background:${sc(p.d)}"></i></span><span class="chv">${ic('chev',18)}</span></button>
    <div class="am-b"><div style="display:flex;gap:8px"><button class="addb" style="margin:0;flex:1" data-act="appedit" data-id="${esc(p.id)}">${ic('edit',16)} ویرایش اپلیکیشن</button><button class="addb" style="margin:0;flex:1" data-act="catnew" data-p="${esc(p.id)}">${ic('plus',16)} دسته جدید</button></div>
     ${p.types.map(t=>`<div class="ac"><div class="ac-h"><b>${esc(t.n)}</b><button class="mini2" data-act="catedit" data-p="${esc(p.id)}" data-t="${esc(t.id)}" aria-label="ویرایش دسته">${ic('edit',16)}</button><button class="mini2 red" data-act="catdel" data-p="${esc(p.id)}" data-t="${esc(t.id)}" aria-label="حذف دسته">${ic('trash',16)}</button></div>
       ${t.items.map(it=>`<div class="ai"><div class="t"><b>${esc(fd(cleanTitle(it.n)))}</b><small>${fa(it.rate)} تومان / هر ۱۰۰۰ • ${fa(it.min)} تا ${fa(it.max)}</small></div><button class="mini2" data-act="itemedit" data-p="${esc(p.id)}" data-t="${esc(t.id)}" data-i="${esc(it.id)}" aria-label="ویرایش">${ic('edit',16)}</button><button class="mini2 red" data-act="itemdel" data-p="${esc(p.id)}" data-t="${esc(t.id)}" data-i="${esc(it.id)}" aria-label="حذف">${ic('trash',16)}</button></div>`).join('')}
       <button class="addb" data-act="itemnew" data-p="${esc(p.id)}" data-t="${esc(t.id)}">${ic('plus',16)} افزودن سرویس</button></div>`).join('')||'<div class="pv" style="text-align:center;margin-top:12px">هنوز دسته‌ای ندارد؛ «دسته جدید» را بزن.</div>'}</div></div>`).join('')}
  `;
}

/* ===== ویرایشگرها ===== */
function openUser(em){
  const u=DB.users[em];
  if(!u)return;const d=dd(em),os=DB.orders.filter(o=>o.u===em),tk=DB.tickets.filter(t=>t.u===em);
  sheet(`<div class="uhero"><img src="${esc(avSrc(u))}" alt=""><div style="min-width:0"><b>${esc(fullOf(u))}</b><small style="direction:rtl">عضو از ${jdate(u.joined)}</small></div></div>
  <div class="pst"><div><b>${fa(d.bal)}</b><span>موجودی (تومان)</span></div><div><b>${fa(os.length)}</b><span>سفارش</span></div><div><b>${fa(tk.length)}</b><span>تیکت</span></div></div>
  <div class="badj"><div class="sh" style="font-size:15px">تغییر موجودی</div>
   <input class="inp" id="bA" inputmode="numeric" placeholder="مبلغ (تومان)" style="text-align:center;font-weight:900;font-size:18px;--tc:var(--brand)">
   <div class="pre" style="margin-top:8px">${[10000,50000,100000,500000].map(v=>`<button data-act="bq" data-v="${v}">${fa(v)}</button>`).join('')}</div>
   <input class="inp" id="bN" placeholder="توضیح (اختیاری، برای کاربر نمایش داده می‌شود)" style="margin-top:10px;--tc:var(--brand)">
   <div class="err" id="bE"></div>
   <div class="two"><button class="btn ok sm" data-act="badd" data-e="${esc(em)}">${ic('plus',18,2.6)} افزایش</button><button class="btn no sm" data-act="bsub" data-e="${esc(em)}">${ic('minus',18,2.6)||''} کاهش</button></div></div>
  <div class="two" style="margin-top:12px"><button class="btn soft sm" data-act="uord" data-e="${esc(em)}">${ic('box',18)} سفارش‌ها</button><button class="btn soft sm" data-act="utk" data-e="${esc(em)}">${ic('ticket',18)} تیکت‌ها</button></div>
  <button class="btn brand full" style="margin-top:10px" data-act="asuser" data-e="${esc(em)}">${ic('user',18)} مشاهده صفحهٔ کاربر</button>`);
}
function adjBal(em,sign){
  const amt=Math.round(num($('#bA').value)),note=$('#bN').value.trim(),e=$('#bE');
  if(amt<=0){e.textContent='مبلغ را وارد کن.';return}
  const d=dd(em);if(sign<0&&amt>d.bal){e.textContent='مبلغ کاهش بیشتر از موجودی کاربر است.';return}
  d.bal+=sign*amt;const base=sign>0?'افزایش موجودی توسط مدیر':'کاهش موجودی توسط مدیر';
  d.tx.unshift({t:note?`${base} — ${note}`:base,a:sign*amt,ts:Date.now()});
  notifyUser(em,`${sign>0?'افزایش':'کاهش'} موجودی: ${fa(amt)} تومان${note?' — '+note:''}`);
  commit();toast(sign>0?'موجودی افزایش یافت':'موجودی کاهش یافت');openUser(em);renderAll();
}
const refDefault=(o,k,p)=>{const left=o.price-(o.rf||0);if(k==='cancel'||k==='refund')return left;if(k==='part')return Math.max(0,Math.min(left,Math.round(o.price*(1-p/100))-(o.rf||0)));return 0};
function openOrdEd(id){
  const o=DB.orders.find(x=>x.id===id);if(!o)return;
  st.oe={id,st:o.st,rfT:false};
  const s=o.st,show=['cancel','refund','part'].includes(s);
  sheet(`<div class="sh">مدیریت سفارش #${fa(o.id)}</div><div class="shp">${esc(fullOf(DB.users[o.u]))} • ${esc(fd(cleanTitle(o.title)))}</div>
  <div class="lbl">وضعیت</div><div class="stg2" id="oeSt">${STS.map(x=>`<button class="${x.wh?'wh':''}" style="${stStyle(x)}" data-act="oest" data-k="${x.k}" aria-pressed="${x.k===s}"><i class="dot"></i>${x.n}</button>`).join('')}</div>
  <div class="lbl"><span>پیشرفت</span><em>تعداد کل: ${fa(o.qty)}</em></div>
  <div class="two"><input class="inp" id="oDn" inputmode="numeric" value="${o.dn}" placeholder="تعداد انجام‌شده" style="--tc:var(--brand);text-align:center;font-weight:900"><input class="inp" id="oPc" inputmode="numeric" value="${pct(o)}" placeholder="درصد" style="--tc:var(--brand);text-align:center;font-weight:900"></div>
  <input type="range" id="oRg" min="0" max="100" value="${pct(o)}" style="width:100%;margin-top:10px;accent-color:var(--brand)">
  <div class="pre">${[0,25,50,75,100].map(v=>`<button data-act="oq" data-v="${v}">${fa(v)}٪</button>`).join('')}</div>
  <div id="rfBox" style="display:${show?'block':'none'}"><div class="lbl"><span>بازگشت وجه به کیف پول (تومان)</span><em>باقی‌ماندهٔ قابل بازگشت: ${fa(o.price-(o.rf||0))}</em></div><input class="inp" id="oRf" inputmode="numeric" value="${refDefault(o,s,pct(o))}" style="--tc:var(--brand)"></div>
  <div class="lbl">توضیح برای کاربر (اختیاری)</div><input class="inp" id="oNt" value="${esc(o.note||'')}" placeholder="مثلاً: ۲۰٪ باقی‌مانده تا فردا تکمیل می‌شود" style="--tc:var(--brand)">
  <div class="err" id="oEe"></div><button class="btn brand full" data-act="osave">${ic('check',20,2.6)} ذخیره</button>`);
}
function oeSync(from){
  const o=DB.orders.find(x=>x.id===st.oe.id);let dn=Math.round(num($('#oDn').value)),p=Math.round(num($('#oPc').value));
  if(from==='dn')p=o.qty?Math.round(dn/o.qty*100):0;
  else if(from==='pc'||from==='rg'){p=from==='rg'?+$('#oRg').value:p;dn=Math.round(o.qty*Math.min(100,p)/100)}
  dn=Math.max(0,Math.min(o.qty,dn));p=Math.max(0,Math.min(100,p));
  if(from!=='dn')$('#oDn').value=dn;if(from!=='pc')$('#oPc').value=p;$('#oRg').value=p;
  if(['cancel','refund','part'].includes(st.oe.st)&&!st.oe.rfT)$('#oRf').value=refDefault(o,st.oe.st,p);
}
function saveOrd(){
  const o=DB.orders.find(x=>x.id===st.oe.id),e=st.oe,er=$('#oEe');
  let dn=Math.max(0,Math.min(o.qty,Math.round(num($('#oDn').value))));if(e.st==='done')dn=o.qty;
  const rf=['cancel','refund','part'].includes(e.st)?Math.max(0,Math.round(num($('#oRf').value))):0;
  if(rf>o.price-(o.rf||0)){er.textContent='مبلغ بازگشتی از مبلغ باقی‌ماندهٔ سفارش بیشتر است.';return}
  const changed=o.st!==e.st;o.st=e.st;o.dn=dn;o.note=$('#oNt').value.trim();
  if(rf>0){const d=dd(o.u);d.bal+=rf;o.rf=(o.rf||0)+rf;d.tx.unshift({t:`بازگشت وجه سفارش #${o.id}`,a:rf,ts:Date.now()});notifyUser(o.u,`${fa(rf)} تومان از سفارش #${fa(o.id)} به کیف پولت برگشت`)}
  if(changed)notifyUser(o.u,`وضعیت سفارش #${fa(o.id)} شد: ${stMeta(e.st).n}`);
  commit();closeSheet();renderAll();toast('سفارش ذخیره شد');
}
function openAppEd(pid){
  const p=pid?PL(pid):{n:'',c:'#6B4EE6',d:'#4B2FD0',img:''};
  st.ed={pid,img:p.img||''};
  sheet(`<div class="sh">${pid?'ویرایش اپلیکیشن':'اپلیکیشن جدید'}</div>
  <div class="pickrow" style="margin-top:8px"><div class="prev" id="alPrev">${logo({...p,img:st.ed.img},84)}</div><div style="flex:1;display:grid;gap:8px"><button class="btn soft sm" data-act="pick" data-t="applogo">${ic('camera',18)} انتخاب لوگو</button>${st.ed.img?`<button class="btn soft sm" data-act="alrm">حذف لوگوی سفارشی</button>`:''}</div></div>
  <div class="lbl">نام اپلیکیشن</div><input class="inp" id="aN" value="${esc(p.n)}" maxlength="30" style="--tc:var(--brand)">
  <div class="two"><div><div class="lbl">رنگ اصلی</div><input type="color" class="clr" id="aC" value="${sc(p.c,'#6B4EE6')}"></div><div><div class="lbl">رنگ دوم</div><input type="color" class="clr" id="aD" value="${sc(p.d,'#4B2FD0')}"></div></div>
  <div class="err" id="aE"></div><button class="btn brand full" data-act="appsave">ذخیره</button>
  ${pid?`<button class="btn soft full" data-act="appdel" data-id="${esc(pid)}" style="margin-top:10px;color:var(--bad)">${ic('trash',18)} حذف اپلیکیشن</button>`:''}`);
}
function saveApp(){
  const n=$('#aN').value.trim(),c=$('#aC').value,d=$('#aD').value,e=$('#aE');
  if(!n){e.textContent='نام اپلیکیشن را بنویس.';return}
  if(st.ed.pid){const p=PL(st.ed.pid);p.n=n;p.c=c;p.d=d;p.img=st.ed.img||''}
  else{const id='a'+uid();prods().push({id,n,c,d,img:st.ed.img||'',types:[]});st.am=id}
  commit();closeSheet();renderAll();toast('ذخیره شد');
}
function openCatEd(pid,tid){
  const p=PL(pid),t=tid?p.types.find(x=>x.id===tid):null;st.ed={pid,tid};
  sheet(`<div class="sh">${t?'ویرایش دسته':'دستهٔ جدید'}</div><div class="lbl">نام دسته</div><input class="inp" id="cN" value="${esc(t?t.n:'')}" maxlength="40" placeholder="مثلاً: ممبر کانال" style="--tc:var(--brand)"><div class="err" id="cE"></div><button class="btn brand full" data-act="catsave">ذخیره</button>`);
}
function openItemEd(pid,tid,iid){
  const p=PL(pid),t=p.types.find(x=>x.id===tid),it=iid?t.items.find(x=>x.id===iid):null;st.ed={pid,tid,iid};
  const rows=it?it.rows.map(r=>`${r[0]}: ${r[1]}`).join('\n'):'';
  sheet(`<div class="sh">${it?'ویرایش سرویس':'سرویس جدید'}</div><div class="shp">${esc(p.n)} • ${esc(t.n)}</div>
  <div class="lbl">عنوان</div><input class="inp" id="iN" value="${esc(it?it.n:'')}" style="--tc:var(--brand)">
  <div class="lbl">قیمت هر ۱۰۰۰ عدد (تومان)</div><input class="inp" id="iR" inputmode="numeric" value="${it?it.rate:''}" style="--tc:var(--brand)">
  <div class="two"><div><div class="lbl">حداقل</div><input class="inp" id="iMn" inputmode="numeric" value="${it?it.min:''}" style="--tc:var(--brand)"></div><div><div class="lbl">حداکثر</div><input class="inp" id="iMx" inputmode="numeric" value="${it?it.max:''}" style="--tc:var(--brand)"></div></div>
  <div class="lbl"><span>مشخصات (هر خط: برچسب: مقدار)</span></div><textarea class="inp" id="iRows" placeholder="زمان تکمیل: 48 تا 72 ساعت&#10;میزان ریزش: 7 روز بدون ریزش" style="--tc:var(--brand)">${esc(rows)}</textarea>
  <div class="lbl"><span>نمونه لینک‌ها (هر خط یکی)</span></div><textarea class="inp" id="iSm" style="--tc:var(--brand);min-height:70px">${esc(it?it.samples.join('\n'):'')}</textarea>
  <div class="lbl"><span>نکات مهم (هر خط یکی)</span></div><textarea class="inp" id="iNt" style="--tc:var(--brand)">${esc(it?it.notes.join('\n'):'')}</textarea>
  <div class="err" id="iE"></div><button class="btn brand full" data-act="itemsave">ذخیره</button>`);
}
function saveItem(){
  const e=st.ed,p=PL(e.pid),t=p.types.find(x=>x.id===e.tid),er=$('#iE');
  const n=$('#iN').value.trim(),rate=num($('#iR').value),mn=num($('#iMn').value),mx=num($('#iMx').value);
  if(!n){er.textContent='عنوان را بنویس.';return}
  if(rate<=0||mn<1||mx<mn){er.textContent='قیمت، حداقل و حداکثر را درست وارد کن (حداکثر ≥ حداقل).';return}
  const lines=s=>s.split('\n').map(x=>x.trim()).filter(Boolean);
  const rows=lines($('#iRows').value).map(l=>{const i=l.search(/[:：]/);return i>0?[l.slice(0,i).trim(),l.slice(i+1).trim()]:null}).filter(Boolean);
  const data={n,rate,min:Math.round(mn),max:Math.round(mx),rows,samples:lines($('#iSm').value),notes:lines($('#iNt').value)};
  if(e.iid)Object.assign(t.items.find(x=>x.id===e.iid),data);else t.items.push({id:'i'+uid(),...data});
  commit();closeSheet();renderAll();toast('ذخیره شد');
}

/* ============ پرداخت کارت‌به‌کارت ============ */
const cardFmt=()=>CARD.num.replace(/(\d{4})(?=\d)/g,'$1 ');
async function copyText(tx,msg){
  try{await navigator.clipboard.writeText(tx)}catch(e){const a=document.createElement('textarea');a.value=tx;a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(_){}a.remove()}
  toast(msg||'کپی شد');
}
function readImg(file,max,cb){
  const r=new FileReader();
  r.onload=()=>{const im=new Image();
    im.onload=()=>{const k=Math.min(1,max/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*k);c.height=Math.round(im.height*k);c.getContext('2d').drawImage(im,0,0,c.width,c.height);cb(c.toDataURL('image/jpeg',.62))};
    im.onerror=()=>toast('این فایل تصویر نیست');im.src=r.result};
  r.readAsDataURL(file);
}
function bankCard(){
  return `<div class="mc bkw"><div class="mc-t"><div class="bk">
   <span class="mc-wm">${arch(3,200)}</span>
   <div class="bk-r"><span class="bk-l">${ic('wallet',16)} کارت به کارت</span><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".85" aria-hidden="true"><path d="M8.5 8.5a5 5 0 0 1 0 7M12 6a8.5 8.5 0 0 1 0 12M15.5 3.5a12 12 0 0 1 0 17"/></svg></div>
   <svg class="mc-chip" width="44" height="32" viewBox="0 0 38 28" aria-hidden="true"><rect width="38" height="28" rx="6" fill="url(#cFace)"/><path d="M0 10h38M0 18h38M13 0v28M25 0v28" stroke="#a85900" stroke-opacity=".35" fill="none"/></svg>
   <div class="bk-num">${cardFmt()}</div>
   <div class="bk-r"><div class="bk-o"><small>به نام</small><b>${CARD.name}</b></div><button class="bk-c" data-act="cpc" aria-label="کپی شماره کارت">${ic('copy',20)}</button></div>
  </div></div></div>`;
}
const stepper=(cur,L)=>`<div class="stp">${L.map((n,i)=>`${i?`<div class="ln ${cur>i?'dn':''}"><b></b></div>`:''}<div class="s ${cur===i+1?'on':cur>i+1?'dn':''}"><i>${cur>i+1?ic('check',16,3):fa(i+1)}</i>${n}</div>`).join('')}</div>`;
const warnCard=()=>`<div class="warnc">${esc(WARN_TXT)}</div>`;
function openPF(kind,o){
  st.pf={kind,step:1,amt:0,o:o||null,img:'',name:full(),last4:'',ref:'',ok:false,pid:null};
  if(kind==='order'){const f=findItem(o.pid,o.tid,o.iid);if(!f){toast('این سرویس دیگر موجود نیست');return}st.pf.amt=price(f.it,o.qty)}
  renderPF();
}
function fmtAmt(n){n=Math.round(+n||0);return n?n.toLocaleString('en-US'):''}
function parseAmt(s){return Math.round(+String(s||'').replace(/[^0-9]/g,'')||0)}
function pf1Charge(){const f=st.pf;return `<div class="sh">چقدر شارژ کنم؟</div><div class="shp">حداقل ${fa(CH_MIN)} و حداکثر ${fa(CH_MAX)} تومان</div>
  <div class="amtbox"><input class="inp" id="pfA" inputmode="numeric" placeholder="مثلاً 100,000" value="${fmtAmt(f.amt)}" autocomplete="off"><span>تومان</span></div>
  <div class="pre" style="margin-top:10px">${[100000,200000,300000,400000,500000].map(v=>`<button data-act="pfamt" data-v="${v}">${fmtAmt(v)}</button>`).join('')}</div>
  <div class="err" id="pfE"></div><button class="btn brand full" data-act="pfnext">ادامه ${ic('chev',18,2.6)}</button>`}
function pf1Order(){
  const f=st.pf,x=findItem(f.o.pid,f.o.tid,f.o.iid);if(!x)return `<div class="sh">این سرویس دیگر موجود نیست</div>`;
  return `<div class="sh">مرور سفارش</div>
  <div class="ps-hero" style="--tc:${sc(x.p.c)};--tc2:${sc(x.p.d)};margin-top:8px">${logo(x.p,52)}<h3>${esc(fd(cleanTitle(x.it.n)))}</h3></div>
  <div class="info" style="margin-top:12px"><div><span>تعداد</span><b>${fa(f.o.qty)}</b></div><div><span>لینک</span><b style="direction:ltr">${esc(f.o.link)}</b></div></div>
  <div class="payamt"><small>مبلغ قابل پرداخت (طبق قیمت محصول)</small><div><b>${fa(f.amt)}</b> <span>تومان</span></div></div>
  <div class="err" id="pfE"></div><button class="btn brand full" data-act="pfnext">ادامه ${ic('chev',18,2.6)}</button>`;
}
function pf2(){const f=st.pf;return `<div class="sh">واریز کارت‌به‌کارت</div><div class="shp">مبلغ را دقیقاً به کارت زیر واریز کن</div>
  ${bankCard()}
  <div class="payamt"><small>مبلغ قابل پرداخت</small><div><b>${fa(f.amt)}</b> <span>تومان</span></div></div>
  <div class="two"><button class="btn soft sm" data-act="cpc">${ic('copy',18)} کپی شماره کارت</button><button class="btn soft sm" data-act="cpa">${ic('copy',18)} کپی مبلغ</button></div>
  ${warnCard()}
  <div class="two" style="margin-top:12px"><button class="btn soft" data-act="pfback">قبلی</button><button class="btn brand" data-act="pfnext">واریز کردم</button></div>`}
function pf3(){const f=st.pf;return `<div class="sh">ارسال فیش واریزی</div><div class="shp">تصویر فیش و اطلاعات واریز را برای پشتیبانی بفرست</div>
  ${f.img?`<div class="upv"><img src="${esc(f.img)}" alt="فیش" data-act="zoom"><div class="two"><button class="btn soft sm" data-act="pfimg">${ic('camera',18)} تغییر عکس</button><button class="btn soft sm" data-act="pfrm">${ic('trash',18)} حذف</button></div></div>`:
   `<button class="up" data-act="pfimg">${ic('upload',34,1.8)}<b>انتخاب عکس فیش</b><small>اسکرین‌شات یا عکس رسید پرداخت</small></button>`}
  <div class="lbl">نام و نام خانوادگی واریزکننده</div><input class="inp" id="pfN" value="${esc(f.name)}" style="--tc:var(--brand)">
  <div class="two"><div><div class="lbl">۴ رقم آخر کارت مبدأ</div><input class="inp ltr" id="pfL" inputmode="numeric" maxlength="4" value="${esc(f.last4)}" placeholder="1234" style="--tc:var(--brand);text-align:center"></div>
  <div><div class="lbl">شماره پیگیری (اختیاری)</div><input class="inp ltr" id="pfR" value="${esc(f.ref)}" style="--tc:var(--brand)"></div></div>
  ${warnCard()}
  <label class="ck"><input type="checkbox" id="pfK" ${f.ok?'checked':''}><span>تأیید می‌کنم که فیش ارسالی واقعی است.</span></label>
  <div class="err" id="pfE"></div>
  <div class="two"><button class="btn soft" data-act="pfback">قبلی</button><button class="btn brand" data-act="pfsend">${ic('send',18)} ارسال برای بررسی</button></div>`}
function pf4(){const f=st.pf;return `<div class="done"><svg viewBox="0 0 52 52" width="92" height="92"><circle cx="26" cy="26" r="23" fill="none" stroke="var(--ok)" stroke-width="3.5"/><path d="M15 27l8 8 14-16" fill="none" stroke="var(--ok)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <b>فیش ارسال شد</b><p>${f.kind==='order'?'سفارش ثبت شد و بعد از تایید پرداخت توسط پشتیبانی در صف انجام قرار می‌گیرد.':'بعد از تایید پشتیبانی، مبلغ به کیف پولت اضافه می‌شود. اگر رد شود، شارژی انجام نمی‌شود.'}</p>
  <div class="payid">کد پیگیری پرداخت: <b>#${fa(f.pid)}</b></div>
  <button class="btn brand full" data-act="pfdone">${f.kind==='order'?'مشاهده سفارش‌ها':'بازگشت به کیف پول'}</button></div>`}
function renderPF(){
  const f=st.pf,L=f.kind==='order'?['مرور سفارش','واریز','ارسال فیش']:['مبلغ','واریز','ارسال فیش'];
  const body=f.step===1?(f.kind==='order'?pf1Order():pf1Charge()):f.step===2?pf2():f.step===3?pf3():pf4();
  sheet(`<div class="pfs">${f.step<4?stepper(f.step,L):''}${body}</div>`,'pf');
}
function pfNext(){
  const f=st.pf,e=$('#pfE');
  if(f.step===1&&f.kind==='charge'){
    if(!f.amt||f.amt<CH_MIN){e.textContent=`حداقل مبلغ شارژ ${fa(CH_MIN)} تومان است.`;return}
    if(f.amt>CH_MAX){e.textContent=`حداکثر مبلغ شارژ ${fa(CH_MAX)} تومان است.`;return}
  }
  f.step++;renderPF();
}
async function submitPay(){
  if(st.pf&&st.pf._busy)return;if(st.pf)st.pf._busy=1;await freshCounters();if(st.pf)st.pf._busy=0;
  reloadDB();const f=st.pf,e=$('#pfE'),name=f.name.trim(),l4=lat(f.last4).trim();
  if(!f.img){e.textContent='عکس فیش واریزی را اضافه کن.';return}
  if(name.length<3){e.textContent='نام و نام خانوادگی واریزکننده را بنویس.';return}
  if(!/^\d{4}$/.test(l4)){e.textContent='۴ رقم آخر کارت مبدأ را به‌صورت عدد وارد کن.';return}
  if(!f.ok){e.textContent='برای ارسال، باید تیک تأیید را بزنی.';return}
  if(DB.pays.filter(p=>p.u===me.email&&p.s==='pending').length>=3){e.textContent='۳ پرداخت در انتظار بررسی داری؛ تا تعیین تکلیف آن‌ها پرداخت جدید ثبت نمی‌شود.';return}
  let ord=null;
  if(f.kind==='charge'){if(f.amt<CH_MIN||f.amt>CH_MAX){e.textContent='مبلغ شارژ مجاز نیست.';return}}
  else{
    const x=findItem(f.o.pid,f.o.tid,f.o.iid);if(!x){e.textContent='این سرویس دیگر موجود نیست.';return}
    if(!f.o.qty||f.o.qty<x.it.min||f.o.qty>x.it.max){e.textContent='تعداد سفارش مجاز نیست.';return}
    f.amt=price(x.it,f.o.qty);
    DB.oid++;ord={id:DB.oid,u:me.email,pid:x.p.id,tid:f.o.tid,iid:x.it.id,title:x.it.n,link:f.o.link,qty:f.o.qty,price:f.amt,dn:0,st:'proc',ts:Date.now(),rf:0,note:'',pay:0};
  }
  DB.payc++;
  const pay={id:DB.payc,u:me.email,kind:f.kind,amt:f.amt,s:'pending',ts:Date.now(),rcpt:f.img,info:{name,last4:l4,ref:f.ref.trim()},oid:ord?ord.id:null,note:''};
  if(ord){ord.pay=pay.id;DB.orders.unshift(ord)}
  DB.pays.unshift(pay);commit();
  notify(ord?`سفارش #${fa(ord.id)} ثبت شد؛ پرداخت در انتظار تایید است`:`درخواست شارژ ${fa(f.amt)} تومان ثبت شد؛ در انتظار تایید است`);
  f.step=4;f.pid=pay.id;renderPF();renderAll();confetti();
}
function payCard(p){
  const s=PAYST[p.s],u=DB.users[p.u],isO=p.kind==='order';
  return `<div class="pass" style="${stStyle(s)}" data-act="pay" data-id="${p.id}" role="button">
   <div class="pass-top"><span class="pass-lg">${ic(isO?'box':'wallet',24)}</span><div class="pass-t"><b>پرداخت #${fa(p.id)}</b><small>${isO?'خرید مستقیم سفارش #'+fa(p.oid):'شارژ کیف پول'} • ${ago(p.ts)}</small></div><span class="spill">${s.n}</span></div>
   <div class="pass-cut"></div>
   <div class="pass-body"><div class="pass-u"><img src="${esc(avSrc(u))}" alt=""><span>${esc(fullOf(u))}</span><small>${esc(p.u)}</small></div>
    <div class="payrow">${p.rcpt?`<img class="thumb" src="${esc(p.rcpt)}" alt="">`:`<span class="thumb ph0">${ic('camera',22)}</span>`}<div class="t"><div class="amt">${fa(p.amt)} <small>تومان</small></div><div class="pv">${esc(p.info.name)} • کارت ****${esc(p.info.last4)}</div></div></div>
   </div></div>`;
}
function renderAPays(){
  const all=DB.pays,cnt=k=>k==='all'?all.length:all.filter(p=>p.s===k).length,f=st.ptab==='all'?all:all.filter(p=>p.s===st.ptab);
  $('#v-a-pays').innerHTML=admHead('پرداخت‌ها',`${fa(cnt('pending'))} پرداخت در انتظار بررسی`,'wallet')+
   `<div class="fbar">${[['pending','در انتظار'],['ok','تایید شده'],['rejected','رد شده'],['all','همه']].map(([k,n])=>`<button class="fc tkc" data-act="ptab" data-id="${k}" aria-pressed="${st.ptab===k}"><i class="dot"></i>${n}<b>${fa(cnt(k))}</b></button>`).join('')}</div>`+
   (f.length?f.map(payCard).join(''):`<div class="empty">${ic('wallet',44,1.5)}پرداختی در این بخش نیست.</div>`);
}
function openPay(id){
  const p=DB.pays.find(x=>x.id===id);if(!p)return;
  const u=DB.users[p.u],s=PAYST[p.s],isO=p.kind==='order',o=isO?DB.orders.find(x=>x.id===p.oid):null;
  sheet(`<div class="sh">پرداخت #${fa(p.id)} <span class="spill2" style="${stStyle(s)}">${s.n}</span></div>
  <div class="shp">${isO?'خرید مستقیم سفارش #'+fa(p.oid):'شارژ کیف پول'} • ${fmt(p.ts)}</div>
  ${p.rcpt?`<img class="rcpt" src="${esc(p.rcpt)}" data-act="zoom" alt="فیش">`:`<div class="empty" style="margin:0">تصویر فیش برای صرفه‌جویی در حافظه پاک شده است.</div>`}
  <div class="info"><div><span>مبلغ</span><b>${fa(p.amt)} تومان</b></div><div><span>کاربر</span><b>${esc(fullOf(u))}</b></div><div><span>ایمیل</span><b style="direction:ltr">${esc(p.u)}</b></div>
   <div><span>نام واریزکننده</span><b>${esc(p.info.name)}</b></div><div><span>۴ رقم آخر کارت مبدأ</span><b>${esc(p.info.last4)}</b></div>${p.info.ref?`<div><span>شماره پیگیری</span><b style="direction:ltr">${esc(p.info.ref)}</b></div>`:''}
   ${o?`<div><span>سفارش</span><b>${esc(fd(cleanTitle(o.title)))} × ${fa(o.qty)}</b></div><div><span>لینک</span><b style="direction:ltr">${esc(o.link)}</b></div>`:''}</div>
  ${p.s==='pending'?`${isO?'':`<div class="lbl">مبلغ قابل شارژ (تومان)</div><input class="inp" id="pyA" inputmode="numeric" value="${p.amt}" style="--tc:var(--brand);text-align:center;font-weight:900">`}
   <div class="lbl">دلیل رد (اختیاری؛ به کاربر نمایش داده می‌شود)</div><input class="inp" id="pyN" placeholder="مثلاً: مبلغ واریزی با فیش مغایرت دارد" style="--tc:var(--brand)">
   <div class="err" id="pyE"></div><div class="two"><button class="btn ok sm" data-act="payok" data-id="${p.id}">${ic('check',18,2.6)} تایید و ثبت</button><button class="btn no sm" data-act="payno" data-id="${p.id}">${ic('x',18,2.6)} رد پرداخت</button></div>`:
   `<div class="onote">${ic('info',16)}<span>${p.s==='ok'?(isO?'پرداخت تایید و سفارش وارد صف شد.':'مبلغ '+fa(p.cr||p.amt)+' تومان به کیف پول کاربر اضافه شد.'):'پرداخت رد شد'+(p.note?': '+esc(p.note):'.')} (${p.rv?fmt(p.rv):''})</span></div>`}
  <button class="btn soft sm" data-act="uview" data-e="${esc(p.u)}" style="margin-top:12px">${ic('user',18)} مدیریت کاربر</button>`);
}
function reviewPay(id,ok){
  const p=DB.pays.find(x=>x.id===id);
  if(!p||p.s!=='pending'){toast('این پرداخت قبلاً بررسی شده');closeSheet();renderAll();return}
  const note=($('#pyN')?$('#pyN').value:'').trim(),isO=p.kind==='order',o=isO?DB.orders.find(x=>x.id===p.oid):null,e=$('#pyE');
  if(ok){
    if(!isO){const a=Math.round(num($('#pyA').value));if(a<=0){e.textContent='مبلغ شارژ را وارد کن.';return}
      p.cr=a;const d=dd(p.u);d.bal+=a;d.tx.unshift({t:'شارژ کارت‌به‌کارت',a,ts:Date.now()});notifyUser(p.u,`پرداخت #${fa(p.id)} تایید شد و ${fa(a)} تومان به کیف پولت اضافه شد`)}
    else{if(o&&o.st==='proc')o.st='queue';notifyUser(p.u,`پرداخت سفارش #${fa(p.oid)} تایید شد و سفارش در صف قرار گرفت`)}
    p.s='ok';
  }else{
    p.s='rejected';p.note=note;
    if(isO&&o){o.st='cancel';o.note=note||'پرداخت تایید نشد'}
    notifyUser(p.u,`پرداخت #${fa(p.id)} تایید نشد${note?': '+note:''}`);
  }
  p.rv=Date.now();DB.pays.filter(x=>x.s!=='pending'&&x.rcpt).slice(20).forEach(x=>x.rcpt='');
  commit();closeSheet();renderAll();toast(ok?'پرداخت تایید شد':'پرداخت رد شد');
}
function zoomImg(src){const z=$('#zoom');z.querySelector('img').src=src;z.classList.add('on')}

/* ============ sheet ها ============ */
function sheet(h,cls){const e=$('#sheet');e.className='sheet '+(cls||'');e.innerHTML=h;$('#sbg').classList.add('on')}
function closeSheet(){$('#sbg').classList.remove('on')}
$('#sbg').addEventListener('click',e=>{if(e.target.id==='sbg')closeSheet()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if($('#sbg').classList.contains('on'))closeSheet();else if(st&&st.tkid)closeChat()}});

function openBell(){
  const L=dd(me.email).notif;
  sheet(`<div class="sh">اعلان‌ها</div>
  ${L.length?`<div class="nlist">${L.map(n=>`<div class="nitem"><div class="nicon">${ic('bell',18)}</div><div class="nbody"><b>${esc(n.t)}</b><small>${n.ts?fmt(n.ts):esc(n.d||'')}</small></div></div>`).join('')}</div>`:
  `<div class="nempty"><div class="nempty-ic">${ic('bell',36)}</div><b>اعلان جدیدی وجود ندارد!</b><small>وقتی وضعیت سفارش یا تیکت عوض شود، اینجا خبر می‌دهیم.</small></div>`}`);
  L.forEach(n=>n.r=0);commit();chrome();
}
function confetti(){
  const cv=$('#fx'),x=cv.getContext('2d');cv.width=innerWidth;cv.height=innerHeight;
  const cols=['#6B4EE6','#F6A823','#14B27F','#E1306C','#2AABEE','#fff'];
  const Q=Array.from({length:110},()=>({x:innerWidth/2,y:innerHeight*.6,vx:(Math.random()-.5)*14,vy:-Math.random()*15-4,s:Math.random()*7+4,c:cols[Math.random()*6|0],r:Math.random()*6}));
  let f=0;(function t(){x.clearRect(0,0,cv.width,cv.height);Q.forEach(p=>{p.vy+=.32;p.x+=p.vx;p.y+=p.vy;p.r+=.2;x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);x.restore()});
    if(++f<110)requestAnimationFrame(t);else x.clearRect(0,0,cv.width,cv.height)})();
}

/* ============ پروفایل ============ */
let pickTarget=null,au={photo:null};
function pickPhoto(target){pickTarget=target;const f=$('#pfile');if(!f)return;f.value='';try{f.click()}catch(e){}setTimeout(()=>{if(pickTarget===target&&f){try{f.click()}catch(e){}}},50)}
function readPhoto(file,size,type,cb){
  const r=new FileReader();
  r.onload=()=>{const im=new Image();
    im.onload=()=>{const c=document.createElement('canvas');c.width=c.height=size;const x=c.getContext('2d'),m=Math.min(im.width,im.height);
      x.drawImage(im,(im.width-m)/2,(im.height-m)/2,m,m,0,0,size,size);cb(c.toDataURL(type,.85))};
    im.onerror=()=>toast('این فایل تصویر نیست');im.src=r.result};
  r.readAsDataURL(file);
}
$('#pfile').addEventListener('change',e=>{
  const input=e.target,f=input.files&&input.files[0],target=pickTarget;
  input.value='';
  if(!f||!target)return;
  if(target==='receipt'){
    const er=$('#pfE');if(er)er.textContent='در حال بارگذاری عکس…';
    readImg(f,900,url=>{
      if(st&&st.pf){st.pf.img=url;renderPF()}
      else toast('عکس آماده شد؛ دوباره تلاش کن');
    });
    return;
  }
  if(target==='applogo'){
    readPhoto(f,160,'image/png',url=>{st.ed.img=url;const p=st.ed.pid?PL(st.ed.pid):{n:$('#aN').value||'?',c:$('#aC').value,d:$('#aD').value};$('#alPrev').innerHTML=logo({...p,n:$('#aN').value||p.n,c:$('#aC').value,d:$('#aD').value,img:url},84)});
    return;
  }
  readPhoto(f,256,'image/jpeg',url=>{if(me){me.avatar=url;mirrorMe();commit();const i=$('#pfPh');if(i)i.src=url;renderAll()}});
});
function openProfile(){
  sheet(`<div class="sh">ویرایش پروفایل</div>
  <div class="pf"><button class="pfb" data-act="pick" data-t="me" aria-label="تغییر عکس"><img id="pfPh" class="avimg" src="${esc(me.avatar||DEF)}" alt=""><span class="cam">${ic('camera',16)}</span></button></div>
  <div class="two" style="margin-top:14px"><div><div class="lbl" style="margin-top:0">نام</div><input class="inp" id="pF" style="--tc:var(--brand)" value="${esc(me.first)}"></div><div><div class="lbl" style="margin-top:0">نام خانوادگی</div><input class="inp" id="pL" style="--tc:var(--brand)" value="${esc(me.last)}"></div></div>
  <div class="err" id="pE"></div>
  <button class="btn brand full" data-act="saveprof">ذخیره</button>
  ${me.avatar?`<button class="btn soft full" data-act="rmphoto" style="margin-top:10px">حذف عکس پروفایل</button>`:''}`);
}
function saveProfile(){
  const f=$('#pF').value.trim(),l=$('#pL').value.trim();
  if(!f||!l){$('#pE').textContent='نام و نام خانوادگی را وارد کن.';return}
  me.first=f;me.last=l;mirrorMe();commit();closeSheet();renderAll();toast('پروفایل ذخیره شد');
}

/* ============ ثبت نام / ورود ============ */
function pwScore(p){let s=0;if(p.length>=6)s++;if(p.length>=9)s++;if(/[A-Za-z]/.test(p)&&/\d/.test(p))s++;if(/[^A-Za-z0-9]/.test(p)||(/[a-z]/.test(p)&&/[A-Z]/.test(p)))s++;return p?Math.max(1,s):0}
function authErr(el,msg){el.innerHTML=msg;const c=$('.au-card');if(c){c.classList.remove('shake');void c.offsetWidth;c.classList.add('shake')}}

let CHL=null;
function chRender(ch){
  const b=$('#cBox');CHL=ch||null;if(!b)return;
  if(!ch){b.innerHTML='';return}
  chHold(ch);
  b.innerHTML='<div id="cQ" style="margin-top:10px;font-weight:700;text-align:center">چالش امنیتی: '+esc(ch.q)+(ch.wait?' <small style="font-weight:400">(حداقل '+lkDigits(ch.wait)+' ثانیه صبر کن)</small>':'')+'</div><label class="fi" style="margin-top:6px"><span class="fic">'+ic('lock',19)+'</span><input class="inp" id="cAns" inputmode="numeric" autocomplete="off" placeholder="پاسخ را به عدد بنویس"></label>';
}
function chHold(ch){
  if(!ch||!ch.wait)return;
  const q=['button[data-act=login]','button[data-act=unlock-pw]'].map(x=>$(x)).filter(Boolean);
  q.forEach(x=>x.disabled=true);
  setTimeout(()=>{const locked=($('#lErr')&&$('#lErr').dataset.lk)||($('#uErr')&&$('#uErr').dataset.lk);if(!locked)q.forEach(x=>{x.disabled=false})},ch.wait*1000+200);
}
function chBody(){return CHL?{captcha_id:CHL.id,captcha_answer:(($('#cAns')||{}).value||'')}:{}}
async function lkRefresh(kind){
  try{
    if(kind==='in'){
      const f=($('#lF').value||'').trim().replace(/\s+/g,' '),l=($('#lL').value||'').trim().replace(/\s+/g,' ');
      if(f&&l){const r=await API.post('/api/lookup',{first:f,last:l});chRender(r.challenge||null)}
    }else{const r=await API.post('/api/session',{});chRender(r.challenge||null)}
  }catch(e){}
}
let LOCKT=null;
const LKS=()=>{try{return JSON.parse(S.g('arka:lk')||'{}')}catch(e){return{}}};
function lkSet(id,sec){const m=LKS();m[id]=Date.now()+sec*1000;S.s('arka:lk',JSON.stringify(m))}
function lkDel(id){const m=LKS();delete m[id];S.s('arka:lk',JSON.stringify(m))}
function lkLeft(id){const e=LKS()[id]||0;return Math.max(0,Math.ceil((e-Date.now())/1000))}
function lkId(f,l){return 'n:'+f+' '+l}
function lkDigits(x){return String(x).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function lkFmt(n){return lkDigits(String(Math.floor(n/60)).padStart(2,'0'))+':'+lkDigits(String(n%60).padStart(2,'0'))}
function lkBtns(kind){return kind==='in'?['button[data-act=login]','button[data-act=login-fp]']:['button[data-act=unlock]','button[data-act=unlock-pw]']}
function lkStop(errSel,kind){clearInterval(LOCKT);LOCKT=null;const el=$(errSel);if(el&&el.dataset.lk){el.innerHTML='';delete el.dataset.lk}lkBtns(kind).forEach(q=>{const b=$(q);if(b)b.disabled=false})}
function lkRun(id,errSel,kind){
  clearInterval(LOCKT);LOCKT=null;
  const tick=()=>{
    const n=lkLeft(id),el=$(errSel);
    if(n<=0){lkDel(id);lkStop(errSel,kind);lkRefresh(kind);return}
    if(el){el.dataset.lk='1';el.innerHTML='محرومیت ورود به‌خاطر چند بار رمز اشتباه — زمان باقی‌مانده: <b dir="ltr" style="font-variant-numeric:tabular-nums">'+lkFmt(n)+'</b>'}
    lkBtns(kind).forEach(q=>{const b=$(q);if(b)b.disabled=true});
  };
  tick();
  if(lkLeft(id)>0)LOCKT=setInterval(tick,1000);
}
function lkFail(err,el,id,kind){
  if(!err||!err.retry)return false;
  lkSet(id,err.retry);
  lkRun(id,'#'+el.id,kind);
  return true;
}
function lkBindLogin(){
  const idNow=()=>lkId(($('#lF').value||'').trim().replace(/\s+/g,' '),($('#lL').value||'').trim().replace(/\s+/g,' '));
  const check=()=>{const id=idNow();if(lkLeft(id)>0)lkRun(id,'#lErr','in');else if(LOCKT||($('#lErr')&&$('#lErr').dataset.lk))lkStop('#lErr','in')};
  ['#lF','#lL'].forEach(q=>{const x=$(q);if(x){x.addEventListener('input',check);x.addEventListener('change',async()=>{
    const f=($('#lF').value||'').trim().replace(/\s+/g,' '),l=($('#lL').value||'').trim().replace(/\s+/g,' ');
    if(!f||!l)return;
    try{const r=await API.post('/api/lookup',{first:f,last:l});chRender(r.challenge||null);if(r.lock>0)lkSet(lkId(f,l),r.lock);else lkDel(lkId(f,l))}catch(e){}
    check();
  })}});
  check();
}
function lkInitUnlock(info){
  const uk=(info&&info.user_key)||'';if(!uk)return;
  chRender(info.challenge||null);
  if(info.lock>0)lkSet(uk,info.lock);else lkDel(uk);
  if(lkLeft(uk)>0)lkRun(uk,'#uErr','un');
}

function isPersianName(s){
  const t=(s||'').trim();
  if(t.length<2)return false;
  if(/[0-9۰-۹٠-٩A-Za-z]/.test(t))return false;
  return /^[\u0600-\u06FF\u200c\s]+$/.test(t);
}
function nameTaken(f,l){
  return Object.values(DB.users).some(u=>u&&u.first===f&&u.last===l&&u.email!==ADMIN_EMAIL);
}
/* ===== احراز هویت: رمز + اثر انگشت اختیاری ===== */
const b64u = buf => {
  const u = buf instanceof ArrayBuffer ? new Uint8Array(buf) : new Uint8Array(buf);
  let s = '';
  for (let i = 0; i < u.length; i++) s += String.fromCharCode(u[i]);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
};
const u8 = b64 => {
  b64 = String(b64 || '').replace(/-/g, '+').replace(/_/g, '/');
  while (b64.length % 4) b64 += '=';
  const bin = atob(b64);
  const o = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) o[i] = bin.charCodeAt(i);
  return o;
};
function fpSupported() {
  return !!(window.PublicKeyCredential && navigator.credentials && window.crypto && window.isSecureContext);
}
function fpHostOk() {
  const h = location.hostname;
  return !!h && !/^\d{1,3}(\.\d{1,3}){3}$/.test(h) && h.indexOf(':') < 0;
}
function fpErr(e) {
  const n = (e && e.name) || '';
  if (n === 'NotAllowedError') return 'اثر انگشت لغو شد. دوباره تلاش کن.';
  if (n === 'InvalidStateError') return 'این اثر انگشت قبلاً ثبت شده.';
  if (n === 'NotSupportedError') return 'این دستگاه اثر انگشت وب را پشتیبانی نمی‌کند.';
  if (n === 'SecurityError') return 'اثر انگشت فقط روی آدرس امن (HTTPS) کار می‌کند.';
  return (e && e.message) || 'خطا در اثر انگشت.';
}
function fpCheckEnv() {
  if (!fpSupported()) throw new Error('اثر انگشت در این محیط در دسترس نیست. می‌توانی فقط با رمز ثبت‌نام کنی.');
  if (!fpHostOk()) throw new Error('برای اثر انگشت، سایت را با آدرس localhost یا دامنهٔ HTTPS باز کن (نه با IP).');
}
async function fpEnroll() {
  fpCheckEnv();
  const o = await API.post('/api/fp/register-options', {});
  const publicKey = {
    challenge: u8(o.challenge),
    rp: { name: 'Arka', id: o.rpId },
    user: { id: u8(o.user.id), name: o.user.name, displayName: o.user.displayName },
    pubKeyCredParams: [{ type: 'public-key', alg: -7 }, { type: 'public-key', alg: -257 }],
    authenticatorSelection: { authenticatorAttachment: 'platform', userVerification: 'required', residentKey: 'discouraged' },
    excludeCredentials: (o.exclude || []).map(id => ({ type: 'public-key', id: u8(id) })),
    timeout: 120000,
    attestation: 'none'
  };
  let cred;
  try {
    cred = await navigator.credentials.create({ publicKey });
  } catch (e1) {
    if (!e1 || e1.name !== 'NotSupportedError') throw new Error(fpErr(e1));
    delete publicKey.authenticatorSelection.authenticatorAttachment;
    try { cred = await navigator.credentials.create({ publicKey }); }
    catch (e2) { throw new Error(fpErr(e2)); }
  }
  if (!cred || !cred.rawId) throw new Error('ثبت اثر انگشت انجام نشد.');
  const rs = cred.response;
  return API.post('/api/fp/register', {
    cid: o.cid, id: b64u(cred.rawId),
    clientDataJSON: b64u(rs.clientDataJSON), attestationObject: b64u(rs.attestationObject)
  });
}
async function fpAssert(userKey) {
  fpCheckEnv();
  const o = await API.post('/api/fp/options', { user_key: userKey });
  const publicKey = {
    challenge: u8(o.challenge), timeout: 120000, userVerification: 'required', rpId: o.rpId,
    allowCredentials: (o.allow || []).map(id => ({ type: 'public-key', id: u8(id) }))
  };
  let ass;
  try { ass = await navigator.credentials.get({ publicKey }); }
  catch (e) { throw new Error(fpErr(e)); }
  if (!ass || !ass.rawId) throw new Error('تأیید اثر انگشت انجام نشد.');
  const rs = ass.response;
  return {
    cid: o.cid, user_key: userKey, id: b64u(ass.rawId),
    clientDataJSON: b64u(rs.clientDataJSON), authenticatorData: b64u(rs.authenticatorData),
    signature: b64u(rs.signature)
  };
}

function renderAuth(mode) {
  const tab = mode || 'up';
  const fpOk = fpSupported();
  $('#auth').innerHTML = `<div class="au" data-tab="${tab}">
   <div class="au-top">
     <button class="ib themeIc" data-act="theme" aria-label="تغییر تم" style="margin:0"></button>
   </div>
   <div class="au-logo"><img src="${ARKA_LOGO}" alt="Arka" width="88" height="88" style="border-radius:22px;object-fit:cover;margin:0 auto;box-shadow:0 12px 28px rgba(0,0,0,.2);display:block">
     <b>آرکا</b><small>Arka</small></div>
   <div class="au-card">
    <div class="seg2"><i class="ind"></i><button data-act="au-tab" data-t="up">ثبت‌نام</button><button data-act="au-tab" data-t="in">ورود</button></div>
    <div class="form up">
      <div class="au-ttl" style="display:block;margin-top:8px"><b>ساخت حساب</b><small>نام و رمز عبور خود را وارد کنید.</small></div>
      <div class="two">
        <label class="fi"><span class="fic">${ic('user',19)}</span><input class="inp" id="sF" placeholder="نام" autocomplete="given-name"></label>
        <label class="fi"><span class="fic">${ic('user',19)}</span><input class="inp" id="sL" placeholder="نام خانوادگی" autocomplete="family-name"></label>
      </div>
      <label class="fi" style="margin-top:10px"><span class="fic">${ic('lock',19)}</span><input class="inp" id="sP" type="password" placeholder="رمز عبور (حداقل ۸ کاراکتر)" autocomplete="new-password"></label>
      <label class="fi" style="margin-top:10px"><span class="fic">${ic('lock',19)}</span><input class="inp" id="sP2" type="password" placeholder="تکرار رمز عبور" autocomplete="new-password"></label>
      <div class="au-err" id="sErr"></div>
      <button class="btn brand full" data-act="signup" id="btnSignup">ثبت‌نام و ورود</button>
    </div>
    <div class="form in">
      <div class="au-ttl" style="display:block;margin-top:8px"><b>ورود به حساب</b><small>با رمز عبور یا اثر انگشت.</small></div>
      <div class="two">
        <label class="fi"><span class="fic">${ic('user',19)}</span><input class="inp" id="lF" placeholder="نام" autocomplete="given-name"></label>
        <label class="fi"><span class="fic">${ic('user',19)}</span><input class="inp" id="lL" placeholder="نام خانوادگی" autocomplete="family-name"></label>
      </div>
      <label class="fi" style="margin-top:10px"><span class="fic">${ic('lock',19)}</span><input class="inp" id="lP" type="password" placeholder="رمز عبور" autocomplete="current-password"></label>
      <div id="cBox"></div>
      <div class="au-err" id="lErr"></div>
      <button class="btn brand full" data-act="login" style="margin-top:8px">ورود با رمز عبور</button>
      <button class="btn soft full" data-act="login-fp" style="margin-top:10px" id="btnLoginFp">ورود با اثر انگشت</button>
    </div>
   </div></div>`;
  $('#auth').classList.add('on');
  syncTheme();
  lkBindLogin();
}

function renderUnlock(info) {
  const name = esc((info && info.name) || 'حساب این دستگاه');
  const uk = esc((info && info.user_key) || '');
  const fpOn = !!(info && info.fp_on);
  $('#auth').innerHTML = `<div class="au unlock-au" data-tab="up">
   <div class="au-top"><button class="ib themeIc" data-act="theme" style="margin:0"></button></div>
   <div class="au-logo"><b>آرکا</b><small>Arka</small></div>
   <div class="au-card unlock-card">
    <div class="unlock-name">${name}</div>
    <div class="au-err" id="uErr"></div>
    <div id="cBox"></div>
    ${fpOn ? `<button type="button" class="btn brand full" data-act="unlock" data-fp="${esc((info && info.fp) || '')}" data-uk="${uk}">ورود با اثر انگشت</button>` : ''}
    <label class="fi" style="margin-top:14px;text-align:start"><span class="fic">${ic('lock',19)}</span><input class="inp" id="uP" type="password" placeholder="رمز عبور" autocomplete="current-password"></label>
    <button type="button" class="btn ${fpOn ? 'soft' : 'brand'} full" style="margin-top:10px" data-act="unlock-pw" data-uk="${uk}">ورود با رمز عبور</button>
   </div></div>`;
  $('#auth').classList.add('on');
  syncTheme();
  lkInitUnlock(info);
}

function setAuthTab(t) { const a = $('.au'); if (a) a.dataset.tab = t; }

async function signup() {
  const f = $('#sF').value.trim().replace(/\s+/g, ' ');
  const l = $('#sL').value.trim().replace(/\s+/g, ' ');
  const pw = ($('#sP') && $('#sP').value) || '';
  const pw2 = ($('#sP2') && $('#sP2').value) || '';
  const e = $('#sErr');
  const useFp = false;
  if (!f || !l) { authErr(e, 'نام و نام خانوادگی را کامل وارد کنید.'); return; }
  if (pw.length < 8) { authErr(e, 'رمز عبور حداقل ۸ کاراکتر باشد.'); return; }
  if (pw !== pw2) { authErr(e, 'تکرار رمز عبور یکسان نیست.'); return; }
  const adminCand = f === 'Arka' && l === 'Member';
  if (!adminCand) {
    if (/[A-Za-z]/.test(f + l)) { authErr(e, 'نام فقط باید با حروف فارسی نوشته شود.'); return; }
    if (!isPersianName(f) || !isPersianName(l)) { authErr(e, 'نام فقط باید با حروف فارسی نوشته شود.'); return; }
  }
  const btn = $('#btnSignup');
  try {
    if (btn) { btn.disabled = true; btn.textContent = 'لطفاً صبر کنید…'; }
    if (btn) btn.textContent = 'ساخت حساب…';
    const r = await API.post('/api/register', {
      first: f, last: l, password: pw, device: deviceId(), fp: '', use_fp: false
    });
    S.s('arka:device', r.user_key);
    window.__ARKA_STATE = await API.get('/api/state').then(x => x.db);
    DB = loadDB();
    enter(r.user_key);
  } catch (err) {
    authErr(e, err.message || 'خطا در ثبت‌نام');
    if (btn) { btn.disabled = false; btn.textContent = 'ثبت‌نام و ورود'; }
  }
}

async function login() {
  const f = $('#lF').value.trim().replace(/\s+/g, ' ');
  const l = $('#lL').value.trim().replace(/\s+/g, ' ');
  const pw = ($('#lP') && $('#lP').value) || '';
  const e = $('#lErr');
  if (!f || !l) { authErr(e, 'نام و نام خانوادگی را وارد کنید.'); return; }
  if (!pw) { authErr(e, 'رمز عبور را وارد کنید.'); return; }
  try {
    const r = await API.post('/api/login', Object.assign({ first: f, last: l, password: pw, device: deviceId() }, chBody()));
    S.s('arka:device', r.user_key);
    window.__ARKA_STATE = r.db || await API.get('/api/state').then(x => x.db);
    DB = loadDB();
    enter(r.user_key);
  } catch (err) {
    if (err.challenge) chRender(err.challenge);
    if (!lkFail(err, e, lkId(f, l), 'in')) authErr(e, err.message || 'ورود ناموفق');
  }
}

async function loginFp() {
  const f = $('#lF').value.trim().replace(/\s+/g, ' ');
  const l = $('#lL').value.trim().replace(/\s+/g, ' ');
  const e = $('#lErr');
  if (!f || !l) { authErr(e, 'نام و نام خانوادگی را وارد کنید.'); return; }
  try {
    const look = await API.post('/api/lookup', { first: f, last: l });
    if (!look.user_key || !look.fp_on) {
      authErr(e, 'برای این حساب اثر انگشت فعال نشده. با رمز وارد شو.');
      return;
    }
    const a = await fpAssert(look.user_key);
    const r = await API.post('/api/fp/login', Object.assign({ device: deviceId() }, a));
    S.s('arka:device', r.user_key);
    S.s('arka:fp', a.id);
    window.__ARKA_STATE = r.db;
    DB = loadDB();
    enter(r.user_key);
  } catch (err) {
    if (!lkFail(err, e, lkId(f, l), 'in')) authErr(e, err.message || 'ورود با اثر انگشت ناموفق');
  }
}

async function unlockFp(fp, uk) {
  const e = $('#uErr');
  try {
    if (!uk) throw new Error('اثر انگشت برای این حساب ثبت نشده.');
    const a = await fpAssert(uk);
    const r = await API.post('/api/fp/login', Object.assign({ device: deviceId() }, a));
    S.s('arka:device', r.user_key);
    S.s('arka:fp', a.id);
    window.__ARKA_STATE = r.db;
    DB = loadDB();
    enter(r.user_key);
  } catch (err) {
    if (!lkFail(err, e, uk, 'un')) authErr(e, err.message || 'تأیید اثر انگشت ناموفق');
  }
}

async function unlockPw(uk) {
  const e = $('#uErr');
  const pw = ($('#uP') && $('#uP').value) || '';
  if (!pw) { authErr(e, 'رمز عبور را وارد کنید.'); return; }
  try {
    const r = await API.post('/api/login', Object.assign({ user_key: uk, password: pw, device: deviceId() }, chBody()));
    S.s('arka:device', r.user_key);
    window.__ARKA_STATE = r.db || await API.get('/api/state').then(x => x.db);
    DB = loadDB();
    enter(r.user_key);
  } catch (err) {
    if (err.challenge) chRender(err.challenge);
    if (!lkFail(err, e, uk, 'un')) authErr(e, err.message || 'رمز نادرست است');
  }
}


async function enableFingerprint(){
  if(!me){toast('اول وارد حساب شو',1);return}
  if(!fpSupported()||!fpHostOk()){
    toast('اثر انگشت فقط روی مرورگر امن (مثلاً Chrome با آدرس https یا localhost) کار می‌کند',1);
    const c=$('#fpHome');if(c)c.checked=false;
    return;
  }
  try{
    toast('حسگر اثر انگشت را لمس کنید…');
    const r = await fpEnroll();
    if(!r||!r.id)throw new Error('ثبت اثر انگشت واقعی انجام نشد');
    me.fp=r.id;me.fp_on=true;
    if(DB.users[me.email]){DB.users[me.email].fp=r.id;DB.users[me.email].fp_on=true}
    S.s('arka:fp',r.id);
    toast('اثر انگشت با موفقیت ثبت شد');
  }catch(err){
    const c=$('#fpHome');if(c)c.checked=false;
    toast(err.message||'ثبت اثر انگشت انجام نشد',1);
  }
  try{renderHome()}catch(e){}
  chrome();
}

async function doLogout(all){
  try{await API.post(all?'/api/logout-all':'/api/logout',{})}catch(e){}
  try{['arka:device','arka:session','arka:token','arka:fp','arka:db','arka:lk'].forEach(k=>S.d(k))}catch(e){}
  window.__CSRF='';
  location.reload();
}
async function disableFingerprint(){
  if(!me)return;
  try{
    await API.post('/api/fp',{enable:false});
    me.fp='';me.fp_on=false;
    if(DB.users[me.email]){DB.users[me.email].fp='';DB.users[me.email].fp_on=false}
    S.d('arka:fp');
    toast('اثر انگشت خاموش شد');
  }catch(err){toast(err.message||'خطا',1)}
  try{renderHome()}catch(e){}
  chrome();
}

function enter(email){
  me=DB.users[email];st={view:'home',tab:'all',ttab:'all',atab:'all',aktab:'all',ptab:'pending',pf:null,pid:null,oc:null,o:null,q:'',fu:null,am:null,cw:0,tkid:null};dd(email);
  S.s('arka:session',email);S.s('arka:sess_ts',String(Date.now()));
  if(email!==ADMIN_EMAIL)S.s('arka:device',email);
  $('#auth').classList.remove('on');
  sweep();nav(isAdmin()?'a-dash':'home');
}
/* ============ مسیریابی و رندر ============ */
function renderAll(){
  if(!st||!me)return;
  document.querySelector('.app')?.classList.toggle('admin-wide',isAdmin()&&!st.viewAs&&st.view==='a-dash');
  if(isAdmin()){renderADash();renderAOrders();renderAPays();renderATickets();renderAUsers();renderAManage()}
  else{renderHome();renderPlat();renderOrders();renderTickets();renderWallet();renderMe()}
  chrome();syncTheme();
  const strip=$('#viewasStrip');
  if(strip){strip.classList.remove('on');document.body.classList.toggle('has-viewas',!!st.viewAs)}
  // در حالت مشاهده، ظاهر اصلی هر صفحه حفظ می‌شود و فقط یک دکمهٔ بازگشت اضافه می‌شود.
  document.querySelectorAll('.viewas-return').forEach(b=>b.remove());
  if(st.viewAs){
    const active=document.querySelector('.view.on');
    const head=active&&active.querySelector('.top');
    if(head){
      const back=document.createElement('button');
      back.type='button';back.className='ib admin-return viewas-return';
      back.dataset.act='asadmin';back.textContent='پنل مدیریت';
      const bell=head.querySelector('[data-act="bell"]');
      if(bell)bell.replaceWith(back);
      else {const host=head.querySelector('.ph,.row');if(host)host.appendChild(back);}
    }
  }
  const junk=$('#viewAsBar');if(junk)junk.remove();
}

function enterUserUI(userKey){
  const u=DB.users[userKey||me.email];
  if(!u){toast('کاربر پیدا نشد');return}
  if(!st._adminBackup)st._adminBackup={email:me.email,role:me.role};
  // کپی کاربر بدون نقش ادمین — دقیقاً مثل کاربر عادی
  me=Object.assign({},u);delete me.role;
  st.viewAs=true;
  st.view='home';st.tab='all';st.ttab='all';st.pid=null;st.oc=null;st.o=null;st.tkid=null;
  closeSheet();
  if(typeof closeChat==='function')try{closeChat()}catch(e){}
  document.querySelectorAll('.view').forEach(v=>v.classList.toggle('on',v.id==='v-home'));
  renderAll();
  window.scrollTo({top:0,behavior:'instant'});
}

function nav(to){
  st.view=to;
  document.querySelectorAll('.view').forEach(v=>v.classList.toggle('on',v.id==='v-'+to));
  renderAll();window.scrollTo({top:0});
}
function refreshLive(){
  if(!st||!me)return;
  const act=document.activeElement;if(act&&/^(INPUT|TEXTAREA)$/.test(act.tagName)&&act.id!=='uQ'&&!$('#tkv').classList.contains('on'))return;
  renderAll();if(st.tkid)renderChat();
}

/* ============ رویدادها ============ */
document.addEventListener('input',e=>{
  const id=e.target.id;
  if(id==='oL'&&st.o)st.o.link=e.target.value;
  else if(id==='oQ'&&st.o){st.o.qty=num(e.target.value);sumUpdate()}
  else if(id==='sP'){const m=$('#sM');if(m)m.dataset.s=pwScore(e.target.value)}
  else if(id==='tkI'){const t=e.target;t.style.height='48px';t.style.height=Math.min(130,t.scrollHeight)+'px'}
  else if(id==='uQ'){st.q=e.target.value;$('#uList').innerHTML=usersHtml()}
  else if(id==='pfA'&&st.pf){const a=parseAmt(e.target.value);st.pf.amt=a;const c=e.target.selectionStart,raw=String(e.target.value).replace(/[^0-9]/g,'');e.target.value=fmtAmt(a);}
  else if(id==='pfN'&&st.pf)st.pf.name=e.target.value;
  else if(id==='pfL'&&st.pf)st.pf.last4=e.target.value;
  else if(id==='pfR'&&st.pf)st.pf.ref=e.target.value;
  else if(id==='pfK'&&st.pf)st.pf.ok=e.target.checked;
  else if(id==='oDn')oeSync('dn');
  else if(id==='oPc')oeSync('pc');
  else if(id==='oRg')oeSync('rg');
  else if(id==='oRf'&&st.oe)st.oe.rfT=true;
  else if(id==='aC'){const d=$('#aD');d.value=shade($('#aC').value,-.28);if(st.ed)updPrev()}
  else if(id==='aD'||id==='aN'){if(st.ed)updPrev()}
  else if(id==='bC1'||id==='bC2')applyBrand($('#bC1').value,$('#bC2').value);
});
function updPrev(){const p=st.ed.pid?PL(st.ed.pid):{};$('#alPrev').innerHTML=logo({...p,id:st.ed.pid?p.id:'new',n:$('#aN').value||p.n||'?',c:$('#aC').value,d:$('#aD').value,img:st.ed.img},84)}
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-act]');if(!t)return;
  if(t.tagName==='A'&&t.getAttribute('href')==='#')e.preventDefault();
  const k=t.dataset,a=k.act;
  if(st&&me&&!['au-tab','eye','theme'].includes(a))reloadDB();
  if(a==='gocharge'){closeSheet();nav('wallet');return}
  switch(a){
    case 'au-tab':setAuthTab(k.t);break;
    case 'pick':pickPhoto(k.t);break;
    case 'eye':{const i=t.parentElement.querySelector('input'),s=i.type==='password';i.type=s?'text':'password';t.innerHTML=ic(s?'eyeoff':'eye',20);break}
    case 'signup':signup();break;
    case 'login':login();break;
    case 'login-fp':loginFp();break;
    case 'fp-on':enableFingerprint();break;
    case 'fp-off':disableFingerprint();break;
    case 'unlock':unlockFp(k.fp,k.uk);break;
    case 'logout':doLogout(false);break;
    case 'logout-all':doLogout(true);break;
    case 'unlock-pw':unlockPw(k.uk);break;
    case 'profile':openProfile();break;
    case 'saveprof':saveProfile();break;
    case 'rmphoto':me.avatar='';mirrorMe();commit();closeSheet();renderAll();toast('عکس پروفایل حذف شد');break;
    case 'userui':{enterUserUI(me.email);break}
    case 'asuser':{enterUserUI(k.e);break}
    
    case 'backupdb':{if(isAdmin())bkDownload(0);break}
    case 'bkrestore':{if(isAdmin())bkPick();break}
    case 'bklist':{if(isAdmin())bkList();break}
    case 'bkdl':{if(isAdmin())bkDownload(+k.id);break}
    case 'bkrs':{if(isAdmin())bkRestore(null,+k.id);break}
    case 'annsend':{annSend();break}
    case 'mged':{if(isAdmin())msgEdit(k.ts);break}
    case 'mgdl':{if(isAdmin())msgDel(k.ts);break}
    case 'tkdel':{tkDelete();break}
case 'asadmin':{if(st._adminBackup){const a=DB.users[st._adminBackup.email];if(a){me=a;st.viewAs=false;st._adminBackup=null;nav('a-dash')}}break}
    case 'flipcard':{const c=t.closest('.mc');if(c)c.classList.toggle('flipped');break}
    case 'nav':nav(k.to);break;
    case 'plat':openPlat(k.id);break;
    case 'cat':{const box=t.closest('.cat'),was=box.classList.contains('open');document.querySelectorAll('.cat.open').forEach(c=>{c.classList.remove('open');c.querySelector('.cat-h').setAttribute('aria-expanded','false')});if(was)st.oc=null;else{box.classList.add('open');t.setAttribute('aria-expanded','true');st.oc=k.id;setTimeout(()=>box.scrollIntoView({behavior:'smooth',block:'nearest'}),60)}break}
    case 'prod':openProd(k.t,k.i);break;
    case 'nt':t.closest('.nt').classList.toggle('open');break;
    case 'qset':{st.o.qty=+k.v;$('#oQ').value=k.v;sumUpdate();break}
    case 'smp':{st.o.link=k.v;$('#oL').value=k.v;break}
    case 'buy':buy();break;
    case 'tab':st.tab=k.id;renderOrders();break;
    case 'reorder':{const o=DB.orders.find(x=>x.id==k.id);if(!o||!findItem(o.pid,o.tid,o.iid)){toast('این سرویس دیگر موجود نیست');break}st.pid=o.pid;openProd(o.tid,o.iid,{pid:o.pid,tid:o.tid,iid:o.iid,link:o.link,qty:o.qty});break}
    case 'tkorder':{const o=DB.orders.find(x=>x.id==k.id);openNewTk({c:'سفارش',s:`سفارش #${fa(o.id)}`});break}
    case 'camt':st.cw=st.cw===+k.v?0:+k.v;renderWallet();break;
    case 'tkcharge':openNewTk({c:'کیف پول',s:'درخواست شارژ کیف پول',m:st.cw?`می‌خواهم کیف پولم ${fa(st.cw)} تومان شارژ شود.`:''});break;
    case 'ttab':st.ttab=k.id;renderTickets();break;
    case 'tknew':openNewTk();break;
    case 'nc':st.nt.c=k.c;document.querySelectorAll('#nCats button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.c===k.c));break;
    case 'tkcreate':createTk();break;
    case 'tkclose2':closeTk(+k.id,'u');openNewTk();renderAll();break;
    case 'tk':openTicket(+k.id);break;
    case 'tkback':closeChat();break;
    case 'tksend':sendTk();break;
    case 'tkclose':closeTk(st.tkid,isAdmin()?'a':'u');renderChat();chrome();break;
    case 'tkopen':reopenTk(st.tkid);renderChat();chrome();break;
    case 'qr':{const ta=$('#tkI');ta.value=QR[+k.i].t;ta.focus();ta.style.height='48px';ta.style.height=Math.min(130,ta.scrollHeight)+'px';break}
    case 'bell':openBell();break;
    case 'pfcharge':openPF('charge');break;
    case 'pfstart':{const o=st.o,f=findItem(o.pid,o.tid,o.iid),er=$('#oE');
      if(!f){er.textContent='این سرویس دیگر موجود نیست.';break}
      if(o.link.trim().length<3){er.textContent='لینک را وارد کن.';break}
      if(!o.qty||o.qty<f.it.min||o.qty>f.it.max||o.qty!==Math.floor(o.qty)){er.textContent=`تعداد باید بین ${fa(f.it.min)} تا ${fa(f.it.max)} باشد.`;break}
      openPF('order',{...o,link:o.link.trim()});break}
    case 'pfamt':{st.pf.amt=+k.v;const i=$('#pfA');if(i)i.value=fmtAmt(+k.v);break}
    case 'pfnext':pfNext();break;
    case 'pfback':st.pf.step--;renderPF();break;
    case 'pfimg':pickPhoto('receipt');break;
    case 'pfrm':st.pf.img='';renderPF();break;
    case 'pfsend':submitPay();break;
    case 'pfdone':closeSheet();nav(st.pf.kind==='order'?'orders':'wallet');break;
    case 'cpc':copyText(CARD.num,'شماره کارت کپی شد');break;
    case 'cpa':copyText(String(st.pf.amt),'مبلغ کپی شد');break;
    case 'zoom':zoomImg(t.src);break;
    case 'zoomx':$('#zoom').classList.remove('on');break;
    case 'ptab':st.ptab=k.id;renderAPays();break;
    case 'pay':openPay(+k.id);break;
    case 'payok':reviewPay(+k.id,true);break;
    case 'payno':reviewPay(+k.id,false);break;
    case 'theme':toggleTheme();break;
    /* ادمین */
    case 'atab':st.atab=k.id;renderAOrders();break;
    case 'aktab':st.aktab=k.id;renderATickets();break;
    case 'fuclr':st.fu=null;renderAOrders();renderATickets();break;
    case 'oedit':openOrdEd(+k.id);break;
    case 'oest':{st.oe.st=k.k;document.querySelectorAll('#oeSt button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===k.k));
      const show=['cancel','refund','part'].includes(k.k);$('#rfBox').style.display=show?'block':'none';
      const o=DB.orders.find(x=>x.id===st.oe.id);if(k.k==='done'){$('#oDn').value=o.qty;oeSync('dn')}
      if(show){st.oe.rfT=false;$('#oRf').value=refDefault(o,k.k,Math.round(num($('#oPc').value)))}break}
    case 'oq':{$('#oPc').value=k.v;oeSync('pc');break}
    case 'osave':saveOrd();break;
    case 'uview':openUser(k.e);break;
    case 'bq':$('#bA').value=k.v;break;
    case 'badd':adjBal(k.e,1);break;
    case 'bsub':adjBal(k.e,-1);break;
    case 'uord':st.fu=k.e;st.atab='all';closeSheet();if(st.tkid)closeChat();nav('a-orders');break;
    case 'utk':st.fu=k.e;st.aktab='all';closeSheet();if(st.tkid)closeChat();nav('a-tickets');break;
    case 'brand':{applyBrand(k.a,k.b);$('#bC1').value=k.a;$('#bC2').value=k.b;document.querySelectorAll('.sw').forEach(s=>s.classList.toggle('on',s===t));break}
    case 'brandsave':DB.settings.brand=$('#bC1').value;DB.settings.brand2=$('#bC2').value;commit();syncTheme();renderAManage();toast('رنگ‌ها ذخیره شد');break;
    case 'amtog':st.am=st.am===k.id?null:k.id;t.closest('.am').classList.toggle('open',st.am===k.id);break;
    case 'appnew':openAppEd(null);break;
    case 'appedit':openAppEd(k.id);break;
    case 'alrm':st.ed.img='';updPrev();break;
    case 'appsave':saveApp();break;
    case 'appdel':if(confirm('این اپلیکیشن با همهٔ دسته‌ها و سرویس‌هایش حذف شود؟')){DB.products=prods().filter(p=>p.id!==k.id);commit();closeSheet();renderAll();toast('حذف شد')}break;
    case 'catnew':openCatEd(k.p,null);break;
    case 'catedit':openCatEd(k.p,k.t);break;
    case 'catsave':{const n=$('#cN').value.trim();if(!n){$('#cE').textContent='نام دسته را بنویس.';break}const p=PL(st.ed.pid);if(st.ed.tid)p.types.find(x=>x.id===st.ed.tid).n=n;else p.types.push({id:'c'+uid(),n,items:[]});commit();closeSheet();renderAll();toast('ذخیره شد');break}
    case 'catdel':if(confirm('این دسته با همهٔ سرویس‌هایش حذف شود؟')){const p=PL(k.p);p.types=p.types.filter(x=>x.id!==k.t);commit();renderAll()}break;
    case 'itemnew':openItemEd(k.p,k.t,null);break;
    case 'itemedit':openItemEd(k.p,k.t,k.i);break;
    case 'itemsave':saveItem();break;
    case 'itemdel':if(confirm('این سرویس حذف شود؟')){const t2=PL(k.p).types.find(x=>x.id===k.t);t2.items=t2.items.filter(x=>x.id!==k.i);commit();renderAll()}break;
  }
});
document.addEventListener('change',e=>{if(e.target.id==='pfK'&&st&&st.pf)st.pf.ok=e.target.checked;if(e.target.id==='fpHome'){if(e.target.checked)enableFingerprint();else disableFingerprint()}});
document.addEventListener('keydown',e=>{
  if(e.key!=='Enter')return;
  if(e.target.id==='tkI'&&(e.ctrlKey||e.metaKey)){e.preventDefault();sendTk()}
  else if(e.target.closest&&e.target.closest('.form')){e.preventDefault();const f=e.target.closest('.form');f.querySelector('.btn[data-act]').click()}
});
/* کارت عضویت: چرخش سه‌بعدی با لمس/ماوس */
function tilt(e){
  const m=e.target.closest&&e.target.closest('.mc'),all=document.querySelectorAll('.mc-t');
  if(!m||m.classList.contains('flipped')){all.forEach(x=>{if(!x.closest('.mc.flipped'))x.style.transform=''});return}
  const r=m.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
  m.querySelector('.mc-t').style.transform=`rotateX(${(-y*12).toFixed(1)}deg) rotateY(${(x*16).toFixed(1)}deg)`;
  m.style.setProperty('--sx',(100-(x+.5)*100)+'%');
}
document.addEventListener('pointermove',tilt);
document.addEventListener('pointerup',()=>document.querySelectorAll('.mc-t').forEach(x=>x.style.transform=''));
/* همگام‌سازی بین تب‌ها + بستن خودکار تیکت‌ها */
window.addEventListener('storage',e=>{if(e.key==='arka:db'){reloadDB();refreshLive()}});
setInterval(()=>{if(!st||!me)return;reloadDB();if(sweep())refreshLive();else chrome()},60000);

/* ============ شروع ============ */
(async function boot(){
  try{S.d('arka:token')}catch(e){}
  try{
    const sess=await API.post('/api/session',{device:deviceId()});
    window.__ARKA_STATE=sess.db||newDB();
    DB=loadDB();
    try{applyBrand(DB.settings.brand,DB.settings.brand2)}catch(x){}
    if(sess.user_key&&sess.user){
      S.s('arka:device',sess.user_key);
      const name=((sess.user.first||'')+' '+(sess.user.last||'')).trim();
      renderUnlock({
        name:name,
        fp:sess.user.fp||S.g('arka:fp')||'',
        user_key:sess.user_key,
        fp_on:!!(sess.fp_on||sess.user.fp_on),
        lock:sess.lock||0,
        challenge:sess.challenge||null
      });
    }else{
      try{['arka:device','arka:session','arka:token','arka:fp','arka:db','arka:lock'].forEach(k=>S.d(k))}catch(e){}
      renderAuth('up');
    }
  }catch(e){
    console.error(e);
    window.__ARKA_STATE=newDB();
    DB=loadDB();
    try{applyBrand(DB.settings.brand,DB.settings.brand2)}catch(x){}
    try{renderAuth('up')}catch(x){console.error(x)}
  }
  try{syncTheme()}catch(x){}
})();

/* اسپلش همیشه تمام می‌شود */
(function(){
  const hide=()=>{const s=document.getElementById('splash');if(s){s.classList.add('off');s.style.pointerEvents='none'}};
  setTimeout(hide,2000);
  setTimeout(hide,4500);
})();
</script>
</body>
</html>
"""


LOGO_JPEG = base64.b64decode("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")

SESSION_TTL = 14 * 24 * 3600
MAX_SESSIONS = 5
LOG_RETENTION = 90 * 24 * 3600
ADVISORY_KEY = 727274001
CHALLENGE_TTL = 120
PBKDF2_ITERS = 600000
PW_MIN, PW_MAX = 8, 128
LEVEL_DECAY = 24 * 3600
MAX_LOCK = 24 * 3600
SOCKET_TIMEOUT = int(os.environ.get("ARKA_SOCKET_TIMEOUT", "20"))
MAX_CONNECTIONS = int(os.environ.get("ARKA_MAX_CONNECTIONS", "256"))
SMALL_BODY = 65536
MAX_BODY = 25 * 1024 * 1024
RATE_WINDOW = 300
CSRF_PATHS = frozenset(("/api/state", "/api/reset", "/api/logout", "/api/logout-all", "/api/fp", "/api/backup/options", "/api/backup/download",
                        "/api/backup/restore", "/api/backup/list",
                        "/api/fp/register-options", "/api/fp/register"))
LOCK_SECONDS = int(os.environ.get("ARKA_LOCK_SECONDS", "300"))
RATE_MAX = 8
SECRET_USER_FIELDS = ("pw", "salt", "pw2", "pass", "password", "fp", "fp_on")
EMPTY_SETTINGS = {"brand": "#6B4EE6", "brand2": "#4B2FD0"}

_hash_slots = threading.BoundedSemaphore(2)

PRODUCTION = os.environ.get("ARKA_PRODUCTION") == "1"
TRUST_PROXY = os.environ.get("ARKA_TRUST_PROXY") == "1"
COOKIE_SECURE = os.environ.get("ARKA_COOKIE_SECURE") == "1"
COOKIE_NAME = "__Host-arka_sid" if PRODUCTION else "arka_sid"
ALLOWED_HOSTS = [h.strip().lower() for h in os.environ.get("ARKA_ALLOWED_HOSTS", "").split(",") if h.strip()]
SKIP_DDL = os.environ.get("ARKA_SKIP_DDL") == "1"
ALERT_WEBHOOK = os.environ.get("ARKA_ALERT_WEBHOOK", "")
ALERT_BALE_TOKEN = os.environ.get("ARKA_ALERT_BALE_TOKEN", "")
ALERT_BALE_CHAT = os.environ.get("ARKA_ALERT_BALE_CHAT", "")
CRITICAL_EVENTS = frozenset(("state_tamper", "reset_denied", "db_reset", "lockout", "csrf_block", "origin_block",
                             "admin_registered", "first_admin_created", "admin_fp_disabled", "admin_fp_removed",
                             "logout_all", "login_burst", "backup_stale", "backup_restore"))
ALERT_INTERVAL = {"backup_stale": 6 * 3600}
CHALLENGE_DELAY_BASE = int(os.environ.get("ARKA_CHALLENGE_DELAY", "3"))
ADMIN_FP_ONLY = (os.environ.get("ARKA_ADMIN_FP_ONLY", "1" if PRODUCTION else "0") == "1")
ALLOW_WEB_ADMIN = (os.environ.get("ARKA_ALLOW_WEB_ADMIN_SIGNUP") == "1") or not PRODUCTION
MIN_VERSIONS = {"argon2-cffi": (23, 1, 0), "psycopg": (3, 2, 0)}
BACKUP_DIR = os.environ.get("ARKA_BACKUP_DIR", "")
BACKUP_MAX_HOURS = int(os.environ.get("ARKA_BACKUP_MAX_HOURS", "48"))
AUTO_BACKUP_HOURS = float(os.environ.get("ARKA_AUTO_BACKUP_HOURS", "12"))
BACKUP_KEEP = int(os.environ.get("ARKA_BACKUP_KEEP", "14"))
BACKUP_SEND_BALE = os.environ.get("ARKA_BACKUP_SEND_BALE") == "1"
RESTORE_FILE = os.environ.get("ARKA_RESTORE_FILE", "")
_alert_last = {}
TESTING = os.environ.get("ARKA_TESTING") == "1"

try:
    import argon2 as _argon2_mod
    from argon2 import PasswordHasher
    from argon2.exceptions import InvalidHashError, VerificationError
    _ph = PasswordHasher()
    ARGON2 = True
    if getattr(_argon2_mod, "__version__", "") == "stub" and not TESTING:
        ARGON2, _ph = False, None
except ImportError:
    _ph = None
    ARGON2 = False
ALLOW_PBKDF2_FALLBACK = os.environ.get("ARKA_ALLOW_PBKDF2") == "1" and not PRODUCTION

try:
    import psycopg
    from psycopg.rows import dict_row
    if getattr(psycopg, "__version__", "") == "test-shim" and not TESTING:
        psycopg = None
except ImportError:
    psycopg = None
    dict_row = None


FONT_DIR = os.environ.get("ARKA_FONT_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_FONT_RE = re.compile(r"^[A-Za-z0-9._\[\]-]{1,80}\.woff2$")
_font_cache = {"t": 0, "files": []}
_WEIGHTS = (("thin", 100), ("extralight", 200), ("ultralight", 200), ("light", 300), ("regular", 400), ("medium", 500),
            ("semibold", 600), ("demibold", 600), ("extrabold", 800), ("bold", 700), ("black", 900), ("heavy", 900))


def font_files():
    now = time.time()
    if now - _font_cache["t"] < 30:
        return _font_cache["files"]
    out = []
    try:
        for name in sorted(os.listdir(FONT_DIR)):
            p = os.path.join(FONT_DIR, name)
            if _FONT_RE.match(name) and os.path.isfile(p) and 0 < os.path.getsize(p) <= 3_000_000:
                out.append(name)
    except OSError:
        out = []
    _font_cache["t"], _font_cache["files"] = now, out
    return out


def font_css():
    blocks = []
    for name in font_files():
        low = name.lower()
        if "[wght]" in low or "variable" in low or "-vf" in low:
            weight = "100 900"
        else:
            weight = next((str(w) for k, w in _WEIGHTS if k in low), "400")
        blocks.append("@font-face{font-family:Vazirmatn;font-style:normal;font-weight:%s;font-display:swap;"
                      "src:url(\"/fonts/%s\") format(\"woff2\")}" % (weight, name.replace("[", "%5B").replace("]", "%5D")))
    return "\n".join(blocks) + "\n"


def database_url():
    direct = os.environ.get("ARKA_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if direct:
        return direct
    path = os.environ.get("ARKA_DATABASE_URL_FILE")
    if path:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read().strip()
        except OSError:
            return ""
    return ""


def secret_file_problem():
    path = os.environ.get("ARKA_DATABASE_URL_FILE")
    if not path or database_url_direct():
        return None
    try:
        st_ = os.stat(path)
    except OSError:
        return "فایل آدرس دیتابیس پیدا نشد: %s" % path
    if st_.st_mode & 0o077:
        return "فایل %s باید فقط برای صاحبش قابل خواندن باشد (chmod 600)." % path
    return None


def database_url_direct():
    return os.environ.get("ARKA_DATABASE_URL") or os.environ.get("DATABASE_URL")


def token_header_allowed():
    return os.environ.get("ARKA_ALLOW_TOKEN_HEADER") == "1" and not PRODUCTION

COMMON_PASSWORDS = frozenset("""
12345678 123456789 1234567890 11111111 00000000 87654321 12341234 123123123 11223344 12121212
password password1 password12 password123 passw0rd p@ssw0rd p@ssword qwertyui qwerty123 qwertyuiop
1q2w3e4r 1q2w3e4r5t 1qaz2wsx qazwsxedc asdfghjk asdfghjkl zxcvbnm1 abc12345 abcd1234 abcdefgh
iloveyou admin123 administrator letmein1 welcome1 welcome123 monkey123 dragon12 football baseball
changeme changeme1 arka1234 arkamember arka12345 09123456789 09121234567 aa123456 a1234567
""".split())


class WebAuthnError(Exception):
    pass


def b64u_enc(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def b64u_dec(s):
    try:
        s = str(s or "")
        return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    except Exception:
        raise WebAuthnError("base64")


def cbor_decode(data, i=0, depth=0):
    try:
        if depth > 8:
            raise WebAuthnError("cbor depth")
        ib = data[i]
        i += 1
        major, info = ib >> 5, ib & 31
        if info < 24:
            val = info
        elif info in (24, 25, 26, 27):
            n = {24: 1, 25: 2, 26: 4, 27: 8}[info]
            if i + n > len(data):
                raise WebAuthnError("cbor short")
            val = int.from_bytes(data[i:i + n], "big")
            i += n
        else:
            raise WebAuthnError("cbor unsupported")
        if major == 0:
            return val, i
        if major == 1:
            return -1 - val, i
        if major in (2, 3):
            if i + val > len(data):
                raise WebAuthnError("cbor short")
            chunk = data[i:i + val]
            i += val
            return (chunk if major == 2 else chunk.decode("utf-8")), i
        if major == 4:
            if val > 256:
                raise WebAuthnError("cbor big")
            arr = []
            for _ in range(val):
                v, i = cbor_decode(data, i, depth + 1)
                arr.append(v)
            return arr, i
        if major == 5:
            if val > 256:
                raise WebAuthnError("cbor big")
            m = {}
            for _ in range(val):
                k, i = cbor_decode(data, i, depth + 1)
                v, i = cbor_decode(data, i, depth + 1)
                m[k] = v
            return m, i
        raise WebAuthnError("cbor type")
    except WebAuthnError:
        raise
    except Exception:
        raise WebAuthnError("cbor")


_P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
_A = _P - 3
_B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
_N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
_G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
      0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


def _ec_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if (y1 + y2) % _P == 0:
            return None
        lam = (3 * x1 * x1 + _A) * pow(2 * y1, -1, _P) % _P
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, _P) % _P
    x3 = (lam * lam - x1 - x2) % _P
    return (x3, (lam * (x1 - x3) - y1) % _P)


def _ec_mul(k, pt):
    r = None
    add = pt
    while k:
        if k & 1:
            r = _ec_add(r, add)
        add = _ec_add(add, add)
        k >>= 1
    return r


def _on_curve(pt):
    x, y = pt
    return 0 <= x < _P and 0 <= y < _P and (y * y - (x * x * x + _A * x + _B)) % _P == 0


def _der_ecdsa(sig):
    try:
        if sig[0] != 0x30:
            raise WebAuthnError("der")
        i = 1
        ln = sig[i]
        i += 1
        if ln & 0x80:
            nb = ln & 0x7f
            ln = int.from_bytes(sig[i:i + nb], "big")
            i += nb
        if i + ln != len(sig):
            raise WebAuthnError("der")
        vals = []
        for _ in range(2):
            if sig[i] != 0x02:
                raise WebAuthnError("der")
            i += 1
            l = sig[i]
            i += 1
            if l & 0x80 or l == 0:
                raise WebAuthnError("der")
            vals.append(int.from_bytes(sig[i:i + l], "big"))
            i += l
        if i != len(sig):
            raise WebAuthnError("der")
        return vals[0], vals[1]
    except WebAuthnError:
        raise
    except Exception:
        raise WebAuthnError("der")


def es256_verify(pub64, msg, sig):
    if len(pub64) != 64:
        return False
    q = (int.from_bytes(pub64[:32], "big"), int.from_bytes(pub64[32:], "big"))
    if not _on_curve(q):
        return False
    try:
        r, s = _der_ecdsa(sig)
    except WebAuthnError:
        return False
    if not (1 <= r < _N and 1 <= s < _N):
        return False
    e = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    w = pow(s, -1, _N)
    pt = _ec_add(_ec_mul(e * w % _N, _G), _ec_mul(r * w % _N, q))
    if pt is None:
        return False
    return pt[0] % _N == r


_SHA256_DIGESTINFO = bytes.fromhex("3031300d060960864801650304020105000420")


def rs256_verify(pub, msg, sig):
    try:
        nl = int.from_bytes(pub[:4], "big")
        n = int.from_bytes(pub[4:4 + nl], "big")
        e = int.from_bytes(pub[4 + nl:], "big")
    except Exception:
        return False
    if n.bit_length() < 2048 or e < 3 or e % 2 == 0 or e > (1 << 32):
        return False
    k = (n.bit_length() + 7) // 8
    if len(sig) != k:
        return False
    sv = int.from_bytes(sig, "big")
    if sv >= n:
        return False
    em = pow(sv, e, n).to_bytes(k, "big")
    pad = k - len(_SHA256_DIGESTINFO) - 32 - 3
    expected = b"\x00\x01" + b"\xff" * pad + b"\x00" + _SHA256_DIGESTINFO + hashlib.sha256(msg).digest()
    return hmac.compare_digest(em, expected)


def parse_auth_data(ad, attested):
    if len(ad) < 37:
        raise WebAuthnError("authData short")
    out = {"rp_hash": ad[:32], "flags": ad[32], "counter": int.from_bytes(ad[33:37], "big")}
    if attested:
        if not out["flags"] & 0x40 or len(ad) < 55:
            raise WebAuthnError("no attested credential")
        clen = int.from_bytes(ad[53:55], "big")
        if clen == 0 or clen > 1023 or 55 + clen > len(ad):
            raise WebAuthnError("bad credential id")
        out["cred_id"] = ad[55:55 + clen]
        cose, _ = cbor_decode(ad, 55 + clen)
        out["cose"] = cose
    return out


def cose_to_pub(cose):
    if not isinstance(cose, dict):
        raise WebAuthnError("cose")
    kty, alg = cose.get(1), cose.get(3)
    if kty == 2 and alg == -7:
        if cose.get(-1) != 1:
            raise WebAuthnError("curve")
        x, y = cose.get(-2), cose.get(-3)
        if not (isinstance(x, bytes) and isinstance(y, bytes) and len(x) == 32 and len(y) == 32):
            raise WebAuthnError("ec key")
        if not _on_curve((int.from_bytes(x, "big"), int.from_bytes(y, "big"))):
            raise WebAuthnError("point not on curve")
        return -7, x + y
    if kty == 3 and alg == -257:
        n, e = cose.get(-1), cose.get(-2)
        if not (isinstance(n, bytes) and isinstance(e, bytes)):
            raise WebAuthnError("rsa key")
        if int.from_bytes(n, "big").bit_length() < 2048:
            raise WebAuthnError("rsa too small")
        return -257, len(n).to_bytes(4, "big") + n + e
    raise WebAuthnError("unsupported algorithm")


def expected_rp_id(handler):
    env = os.environ.get("ARKA_RP_ID", "").strip().lower()
    if env:
        return env
    host = (handler.headers.get("Host") or "").strip().lower()
    if host.startswith("["):
        return host.split("]")[0] + "]"
    return host.split(":")[0]


def check_client_data(raw, typ, challenge, rp_id):
    try:
        cd = json.loads(raw.decode("utf-8"))
    except Exception:
        raise WebAuthnError("clientData")
    if not isinstance(cd, dict) or cd.get("type") != typ:
        raise WebAuthnError("type")
    got = b64u_dec(cd.get("challenge"))
    if not hmac.compare_digest(got, challenge):
        raise WebAuthnError("challenge")
    if cd.get("crossOrigin"):
        raise WebAuthnError("crossOrigin")
    origin = str(cd.get("origin") or "")
    pu = urlparse(origin)
    host = (pu.hostname or "").lower()
    fixed = os.environ.get("ARKA_ORIGIN", "").strip().rstrip("/")
    if fixed and origin != fixed:
        raise WebAuthnError("origin")
    if not (host == rp_id or host.endswith("." + rp_id)):
        raise WebAuthnError("origin")
    if not (pu.scheme == "https" or (pu.scheme == "http" and host == "localhost")):
        raise WebAuthnError("origin scheme")


def check_flags(ad):
    if not ad["flags"] & 0x01:
        raise WebAuthnError("user not present")
    if not ad["flags"] & 0x04:
        raise WebAuthnError("user not verified")


def verify_registration(rp_id, challenge, body):
    client = b64u_dec(body.get("clientDataJSON"))
    att = b64u_dec(body.get("attestationObject"))
    check_client_data(client, "webauthn.create", challenge, rp_id)
    obj, _ = cbor_decode(att)
    if not isinstance(obj, dict) or not isinstance(obj.get("authData"), bytes):
        raise WebAuthnError("attestation")
    ad = parse_auth_data(obj["authData"], True)
    if not hmac.compare_digest(ad["rp_hash"], hashlib.sha256(rp_id.encode()).digest()):
        raise WebAuthnError("rpIdHash")
    check_flags(ad)
    alg, pub = cose_to_pub(ad["cose"])
    cred_id = b64u_enc(ad["cred_id"])
    if body.get("id") and body.get("id") != cred_id:
        raise WebAuthnError("credential id mismatch")
    return cred_id, alg, pub, ad["counter"]


def verify_assertion(rp_id, challenge, cred, body):
    client = b64u_dec(body.get("clientDataJSON"))
    adraw = b64u_dec(body.get("authenticatorData"))
    sig = b64u_dec(body.get("signature"))
    check_client_data(client, "webauthn.get", challenge, rp_id)
    ad = parse_auth_data(adraw, False)
    if not hmac.compare_digest(ad["rp_hash"], hashlib.sha256(rp_id.encode()).digest()):
        raise WebAuthnError("rpIdHash")
    check_flags(ad)
    msg = adraw + hashlib.sha256(client).digest()
    if cred["alg"] == -7:
        ok = es256_verify(bytes(cred["pub"]), msg, sig)
    elif cred["alg"] == -257:
        ok = rs256_verify(bytes(cred["pub"]), msg, sig)
    else:
        ok = False
    if not ok:
        raise WebAuthnError("bad signature")
    old = cred["sign_count"]
    if (old or ad["counter"]) and ad["counter"] <= old:
        raise WebAuthnError("counter replay")
    return ad["counter"]


def new_challenge(purpose, user_key):
    now = time.time()
    cid = secrets.token_urlsafe(16)
    ch = secrets.token_bytes(32)
    with _lock:
        c = db_conn()
        c.execute("DELETE FROM challenges WHERE exp<?", (now,))
        c.execute("INSERT INTO challenges(cid,ch,purpose,user_key,exp) VALUES(?,?,?,?,?)",
                  (cid, ch, purpose, user_key, now + CHALLENGE_TTL))
        n = c.execute("SELECT COUNT(*) AS n FROM challenges").fetchone()["n"]
        if n > 20000:
            c.execute("DELETE FROM challenges WHERE cid IN (SELECT cid FROM challenges ORDER BY exp LIMIT 5000)")
        c.commit()
        c.close()
    return cid, ch


def take_challenge(cid, purpose, user_key):
    with _lock:
        c = db_conn()
        row = c.execute("DELETE FROM challenges WHERE cid=? RETURNING ch,purpose,user_key,exp", (str(cid or ""),)).fetchone()
        c.commit()
        c.close()
    if not row or row["exp"] < time.time() or row["purpose"] != purpose or row["user_key"] != user_key:
        raise WebAuthnError("challenge expired")
    return bytes(row["ch"])


def lock_remaining(key):
    now = time.time()
    with _lock:
        c = db_conn()
        row = c.execute("SELECT until_ts FROM locks WHERE key=?", (key,)).fetchone()
        c.close()
    if row and row["until_ts"] > now:
        return int(row["until_ts"] - now) + 1
    return 0


def rate_blocked(key, limit=None):
    now = time.time()
    wait = 0
    with _lock:
        c = db_conn()
        row = c.execute("SELECT until_ts FROM locks WHERE key=?", (key,)).fetchone()
        if row and row["until_ts"] > now:
            c.close()
            return int(row["until_ts"] - now) + 1
        if row:
            c.execute("DELETE FROM locks WHERE key=?", (key,))
        n = c.execute("SELECT COUNT(*) AS n FROM rate_events WHERE key=? AND ts>?",
                      (key, now - RATE_WINDOW)).fetchone()["n"]
        if n >= (limit or RATE_MAX):
            lv = c.execute("SELECT level,ts FROM lock_levels WHERE key=?", (key,)).fetchone()
            level = lv["level"] + 1 if lv and now - lv["ts"] < LEVEL_DECAY else 0
            wait = int(min(LOCK_SECONDS * (2 ** min(level, 20)), MAX_LOCK))
            c.execute("INSERT INTO lock_levels(key,level,ts) VALUES(?,?,?) "
                      "ON CONFLICT(key) DO UPDATE SET level=excluded.level, ts=excluded.ts", (key, level, now))
            c.execute("INSERT INTO locks(key,until_ts) VALUES(?,?) "
                      "ON CONFLICT(key) DO UPDATE SET until_ts=excluded.until_ts", (key, now + wait))
            c.execute("DELETE FROM rate_events WHERE key=?", (key,))
        c.commit()
        c.close()
    if wait:
        log_event("lockout", detail={"key_kind": key.split(":")[0], "seconds": wait})
    return wait


_FA = "۰۱۲۳۴۵۶۷۸۹"


def _fa(n):
    return str(n).translate({ord(str(i)): _FA[i] for i in range(10)})


def _ascii_digits(t):
    return str(t).translate({ord(_FA[i]): str(i) for i in range(10)} | {ord("٠١٢٣٤٥٦٧٨٩"[i]): str(i) for i in range(10)}).strip()


def captcha_level(acct_key, ip):
    now = time.time()
    with _lock:
        c = db_conn()
        a = c.execute("SELECT level FROM lock_levels WHERE key=? AND ts>?", ("lacct:" + acct_key, now - LEVEL_DECAY)).fetchone()
        i = c.execute("SELECT level FROM lock_levels WHERE key=? AND ts>?", ("lip:" + ip, now - LEVEL_DECAY)).fetchone()
        c.close()
    return max(a["level"] if a else -1, i["level"] if i else -1)


def make_captcha(level=0):
    if level >= 2:
        a, b, c3 = 2 + secrets.randbelow(8), 2 + secrets.randbelow(8), 2 + secrets.randbelow(19)
        if secrets.randbelow(2):
            q, ans = "%s × %s + %s" % (_fa(a), _fa(b), _fa(c3)), a * b + c3
        else:
            q, ans = "%s × %s − %s" % (_fa(a), _fa(b), _fa(c3)), a * b - c3
            if ans < 0:
                q, ans = "%s × %s + %s" % (_fa(a), _fa(b), _fa(c3)), a * b + c3
    else:
        kind = secrets.randbelow(3)
        if kind == 0:
            a, b = 2 + secrets.randbelow(18), 2 + secrets.randbelow(18)
            q, ans = "%s + %s" % (_fa(a), _fa(b)), a + b
        elif kind == 1:
            a, b = 2 + secrets.randbelow(18), 2 + secrets.randbelow(18)
            a, b = max(a, b), min(a, b)
            q, ans = "%s − %s" % (_fa(a), _fa(b)), a - b
        else:
            a, b = 2 + secrets.randbelow(8), 2 + secrets.randbelow(8)
            q, ans = "%s × %s" % (_fa(a), _fa(b)), a * b
    delay = min(CHALLENGE_DELAY_BASE + 2 * max(level, 0), 20) if CHALLENGE_DELAY_BASE > 0 else 0
    cid = secrets.token_urlsafe(12)
    now = time.time()
    with _lock:
        c = db_conn()
        c.execute("INSERT INTO challenges(cid,ch,purpose,user_key,exp) VALUES(?,?,?,?,?)",
                  (cid, ("%d:%.3f" % (ans, now + delay)).encode("ascii"), "captcha", "", now + 300 + delay))
        c.commit()
        c.close()
    return {"id": cid, "q": q + " = ؟", "wait": delay}


def check_captcha(cid, answer):
    if not isinstance(cid, str) or not isinstance(answer, (str, int)) or isinstance(answer, bool):
        return "wrong"
    with _lock:
        c = db_conn()
        row = c.execute("DELETE FROM challenges WHERE cid=? AND purpose=? RETURNING ch,exp", (cid, "captcha")).fetchone()
        c.commit()
        c.close()
    if not row or row["exp"] < time.time():
        return "wrong"
    try:
        want, not_before = bytes(row["ch"]).decode("ascii").split(":")
    except Exception:
        return "wrong"
    if not hmac.compare_digest(want.encode("ascii"), _ascii_digits(answer).encode("ascii", "replace")):
        return "wrong"
    if time.time() + 0.01 < float(not_before):
        return "early"
    return "ok"


def decoy_key(first, last):
    return "u" + hmac.new(_CSRF_SECRET["k"] or b"x", ("n:%s %s" % (first, last)).encode("utf-8", "replace"),
                          hashlib.sha256).hexdigest()[:12]


def needs_challenge(acct_key, ip):
    now = time.time()
    with _lock:
        c = db_conn()
        a = c.execute("SELECT level FROM lock_levels WHERE key=? AND ts>?", ("lacct:" + acct_key, now - LEVEL_DECAY)).fetchone()
        i = c.execute("SELECT level FROM lock_levels WHERE key=? AND ts>?", ("lip:" + ip, now - LEVEL_DECAY)).fetchone()
        c.close()
    return bool(a) or bool(i and i["level"] >= 1)


def challenge_for(acct_key, ip):
    if needs_challenge(acct_key, ip) and not throttled("ch:" + ip, 60):
        return make_captcha(captcha_level(acct_key, ip))
    return None


def attempt_gate(key, limit):
    now = time.time()
    wait = 0
    with _lock:
        c = db_conn()
        row = c.execute("SELECT until_ts FROM locks WHERE key=?", (key,)).fetchone()
        if row and row["until_ts"] > now:
            c.close()
            return int(row["until_ts"] - now) + 1
        if row:
            c.execute("DELETE FROM locks WHERE key=?", (key,))
        c.execute("INSERT INTO rate_events(key,ts) VALUES(?,?)", (key, now))
        n = c.execute("SELECT COUNT(*) AS n FROM rate_events WHERE key=? AND ts>?", (key, now - RATE_WINDOW)).fetchone()["n"]
        if n > limit:
            lv = c.execute("SELECT level,ts FROM lock_levels WHERE key=?", (key,)).fetchone()
            level = lv["level"] + 1 if lv and now - lv["ts"] < LEVEL_DECAY else 0
            wait = int(min(LOCK_SECONDS * (2 ** min(level, 20)), MAX_LOCK))
            c.execute("INSERT INTO lock_levels(key,level,ts) VALUES(?,?,?) "
                      "ON CONFLICT(key) DO UPDATE SET level=excluded.level, ts=excluded.ts", (key, level, now))
            c.execute("INSERT INTO locks(key,until_ts) VALUES(?,?) "
                      "ON CONFLICT(key) DO UPDATE SET until_ts=excluded.until_ts", (key, now + wait))
            c.execute("DELETE FROM rate_events WHERE key=?", (key,))
        c.commit()
        c.close()
    if wait:
        log_event("lockout", detail={"key_kind": key.split(":")[0], "seconds": wait})
    return wait


def rate_release(key):
    with _lock:
        c = db_conn()
        row = c.execute("SELECT MAX(ts) AS m FROM rate_events WHERE key=?", (key,)).fetchone()
        if row and row["m"] is not None:
            c.execute("DELETE FROM rate_events WHERE key=? AND ts=?", (key, row["m"]))
        c.commit()
        c.close()


def throttled(key, limit, window=60):
    now = time.time()
    with _lock:
        c = db_conn()
        n = c.execute("SELECT COUNT(*) AS n FROM rate_events WHERE key=? AND ts>?", (key, now - window)).fetchone()["n"]
        if n >= limit:
            c.close()
            return True
        c.execute("INSERT INTO rate_events(key,ts) VALUES(?,?)", (key, now))
        c.commit()
        c.close()
    return False


def rate_fail(key):
    with _lock:
        c = db_conn()
        c.execute("INSERT INTO rate_events(key,ts) VALUES(?,?)", (key, time.time()))
        if secrets.randbelow(50) == 0:
            c.execute("DELETE FROM rate_events WHERE ts<?", (time.time() - RATE_WINDOW,))
        c.commit()
        c.close()


def rate_ok(key):
    with _lock:
        c = db_conn()
        c.execute("DELETE FROM rate_events WHERE key=?", (key,))
        c.execute("DELETE FROM locks WHERE key=?", (key,))
        c.execute("DELETE FROM lock_levels WHERE key=?", (key,))
        c.commit()
        c.close()


def reset_rate_limits():
    with _lock:
        c = db_conn()
        c.execute("DELETE FROM rate_events")
        c.execute("DELETE FROM locks")
        c.execute("DELETE FROM lock_levels")
        c.commit()
        c.close()


def _pbkdf2_encode(pw):
    salt = secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, PBKDF2_ITERS)
    return "pbkdf2v2$%d$%s$%s" % (PBKDF2_ITERS, b64u_enc(salt), b64u_enc(h))


def hash_pw(pw):
    if ARGON2:
        with _hash_slots:
            return _ph.hash(pw)
    if ALLOW_PBKDF2_FALLBACK:
        with _hash_slots:
            return _pbkdf2_encode(pw)
    raise RuntimeError("argon2-cffi is not installed")


def _verify_legacy(u, pw):
    stored = u.get("pw") or ""
    salt = u.get("salt") or ""
    try:
        if stored.startswith("pbkdf2v2$"):
            _, it, s64, h64 = stored.split("$")
            got = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), b64u_dec(s64), int(it))
            return hmac.compare_digest(got, b64u_dec(h64))
        if stored.startswith("pbkdf2$"):
            _, it, h = stored.split("$", 2)
            got = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(salt), int(it)).hex()
            return hmac.compare_digest(got, h)
        if stored:
            got = hashlib.sha256((salt + pw).encode("utf-8")).hexdigest()
            return hmac.compare_digest(got, stored)
        plain = u.get("password")
        if plain:
            return hmac.compare_digest(str(plain).encode("utf-8"), pw.encode("utf-8"))
    except Exception:
        pass
    return False


def check_pw(u, pw):
    stored = u.get("pw") or ""
    if stored.startswith("$argon2"):
        if not ARGON2:
            return False, False
        try:
            with _hash_slots:
                _ph.verify(stored, pw)
                return True, bool(_ph.check_needs_rehash(stored))
        except (VerificationError, InvalidHashError):
            return False, False
    ok = _verify_legacy(u, pw)
    return ok, ok


_DUMMY = {}


def burn_dummy_verify(pw):
    if not ARGON2:
        return
    if "h" not in _DUMMY:
        _DUMMY["h"] = hash_pw(secrets.token_urlsafe(12))
    try:
        with _hash_slots:
            _ph.verify(_DUMMY["h"], pw)
    except Exception:
        pass


def password_problem(pw, first="", last=""):
    if not isinstance(pw, str) or not pw:
        return "رمز عبور را وارد کنید."
    if len(pw) < PW_MIN:
        return "رمز عبور حداقل ۸ کاراکتر باشد."
    if len(pw) > PW_MAX:
        return "رمز عبور خیلی طولانی است."
    if re.search(r"[\x00-\x1f\x7f]", pw):
        return "رمز عبور شامل کاراکتر نامعتبر است."
    low = pw.lower()
    if low in COMMON_PASSWORDS or len(set(low)) < 3:
        return "این رمز عبور خیلی رایج و ناامن است؛ رمز دیگری انتخاب کن."
    if low in (first.lower(), last.lower(), (first + last).lower(), (first + " " + last).lower()):
        return "رمز عبور نباید با نام تو یکسان باشد."
    return None


def name_ok(v):
    return isinstance(v, str) and 0 < len(v) <= 40 and not re.search(r"[\x00-\x1f\x7f<>\"'&`\\]", v)


def token_hash(token):
    return hashlib.sha256(str(token).encode("utf-8")).hexdigest()


def _clean(p):
    if isinstance(p, str):
        p = p.replace("\x00", "\ufffd")
        try:
            p.encode("utf-8")
        except UnicodeEncodeError:
            p = p.encode("utf-8", "replace").decode("utf-8")
    return p


_tl = threading.local()


class _Conn:
    def __init__(self, pool, raw):
        self._pool, self._raw, self._done = pool, raw, False

    def execute(self, sql, params=()):
        return self._raw.execute(sql.replace("?", "%s"), tuple(_clean(p) for p in params))

    def commit(self):
        self._raw.commit()

    def rollback(self):
        self._raw.rollback()

    def close(self):
        if not self._done:
            self._done = True
            lst = getattr(_tl, "open", [])
            if self in lst:
                lst.remove(self)
            self._pool.release(self._raw)


class _Pool:
    def __init__(self, size=10):
        self._idle, self._used, self._mx = [], {}, size
        self._sem = threading.BoundedSemaphore(size)
        self._mu = threading.Lock()

    def get(self):
        if psycopg is None:
            raise RuntimeError("psycopg is not installed")
        if not self._sem.acquire(timeout=15):
            raise RuntimeError("database busy")
        try:
            raw = None
            while True:
                with self._mu:
                    raw = self._idle.pop() if self._idle else None
                if raw is None:
                    break
                if raw.closed or raw.broken:
                    continue
                if time.time() - self._used.get(id(raw), 0) > 30:
                    try:
                        raw.execute("SELECT 1")
                        raw.rollback()
                    except Exception:
                        try:
                            raw.close()
                        except Exception:
                            pass
                        continue
                break
            if raw is None:
                raw = psycopg.connect(database_url(), row_factory=dict_row, autocommit=False, connect_timeout=10)
            c = _Conn(self, raw)
            if not hasattr(_tl, "open"):
                _tl.open = []
            _tl.open.append(c)
            return c
        except BaseException:
            self._sem.release()
            raise

    def release(self, raw):
        try:
            raw.rollback()
            ok = not raw.closed and not raw.broken
        except Exception:
            ok = False
        with self._mu:
            self._used[id(raw)] = time.time()
            if ok and len(self._idle) < self._mx:
                self._idle.append(raw)
                ok = None
        if ok is not None:
            try:
                raw.close()
            except Exception:
                pass
        self._sem.release()

    def close_all(self):
        with self._mu:
            idle, self._idle = self._idle, []
        for raw in idle:
            try:
                raw.close()
            except Exception:
                pass


_pool = _Pool()


def db_conn():
    return _pool.get()


def close_pool():
    _pool.close_all()


def release_thread_conns():
    for c in list(getattr(_tl, "open", [])):
        try:
            c.close()
        except Exception:
            pass


class StateLock:
    def __init__(self):
        self._r = threading.RLock()
        self._d = threading.local()
        self._conn = None

    def _take(self):
        for attempt in (0, 1):
            try:
                if self._conn is None or self._conn.closed:
                    self._conn = psycopg.connect(database_url(), autocommit=True, connect_timeout=10)
                self._conn.execute("SELECT pg_advisory_lock(%s)", (ADVISORY_KEY,))
                return
            except Exception:
                try:
                    if self._conn is not None:
                        self._conn.close()
                except Exception:
                    pass
                self._conn = None
                if attempt:
                    raise

    def _drop(self):
        try:
            self._conn.execute("SELECT pg_advisory_unlock(%s)", (ADVISORY_KEY,))
        except Exception:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def __enter__(self):
        self._r.acquire()
        n = getattr(self._d, "n", 0)
        if n == 0:
            try:
                self._take()
            except BaseException:
                self._r.release()
                raise
        self._d.n = n + 1
        return self

    def __exit__(self, *exc):
        self._d.n -= 1
        try:
            if self._d.n == 0:
                self._drop()
        finally:
            self._r.release()
        return False


_lock = StateLock()
_CSRF_SECRET = {"k": None}


def csrf_for(token):
    if not _CSRF_SECRET["k"] or not token:
        return ""
    return hmac.new(_CSRF_SECRET["k"], str(token).encode("utf-8"), hashlib.sha256).hexdigest()


def _send_alert(text):
    targets = []
    if ALERT_WEBHOOK:
        targets.append((ALERT_WEBHOOK, {"text": text}))
    if ALERT_BALE_TOKEN and ALERT_BALE_CHAT:
        targets.append(("https://tapi.bale.ai/bot%s/sendMessage" % ALERT_BALE_TOKEN,
                        {"chat_id": ALERT_BALE_CHAT, "text": text}))
    for url, body in targets:
        host = (urlparse(url).hostname or "").lower()
        if not (url.startswith("https://") or (url.startswith("http://") and host in ("localhost", "127.0.0.1"))):
            continue
        try:
            req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=6).read()
        except Exception:
            pass


def alert(event, uk=None, ip=None, detail=None):
    text = "Arka alert: %s | user=%s | ip=%s | %s" % (event, uk or "-", ip or "-",
                                                         json.dumps(detail or {}, ensure_ascii=False)[:300])
    try:
        sys.stderr.write("ALERT " + text + "\n")
    except Exception:
        pass
    if not (ALERT_WEBHOOK or (ALERT_BALE_TOKEN and ALERT_BALE_CHAT)):
        return
    now = time.time()
    if now - _alert_last.get(event, 0) < ALERT_INTERVAL.get(event, 300):
        return
    _alert_last[event] = now
    threading.Thread(target=_send_alert, args=(text,), daemon=True).start()


def log_event(event, uk=None, ip=None, detail=None):
    detail = detail or {}
    if event in CRITICAL_EVENTS:
        alert(event, uk, ip, detail)
    try:
        sys.stderr.write("SEC " + json.dumps({"ts": int(time.time()), "event": event, "user": uk, "ip": ip,
                                              "detail": detail}, ensure_ascii=False) + "\n")
        with _lock:
            c = db_conn()
            c.execute("INSERT INTO security_log(ts,event,user_key,ip,detail) VALUES(?,?,?,?,?)",
                      (time.time(), event, uk, ip, json.dumps(detail, ensure_ascii=False)[:1000]))
            c.commit()
            c.close()
    except Exception:
        pass


def empty_state():
    return {
        "v": 3, "users": {}, "data": {}, "orders": [], "tickets": [],
        "tid": 0, "oid": 0, "pays": [], "payc": 0, "products": None,
        "settings": dict(EMPTY_SETTINGS),
    }


SCHEMA = [
    "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS devices (device_id TEXT PRIMARY KEY, user_key TEXT NOT NULL, created DOUBLE PRECISION NOT NULL)",
    "CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, user_key TEXT NOT NULL, device_id TEXT, created DOUBLE PRECISION NOT NULL)",
    "CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_key)",
    "CREATE TABLE IF NOT EXISTS webauthn_creds (cred_id TEXT PRIMARY KEY, user_key TEXT NOT NULL, alg INTEGER NOT NULL, "
    "pub BYTEA NOT NULL, sign_count BIGINT NOT NULL, created DOUBLE PRECISION NOT NULL)",
    "CREATE INDEX IF NOT EXISTS idx_cred_user ON webauthn_creds(user_key)",
    "CREATE TABLE IF NOT EXISTS locks (key TEXT PRIMARY KEY, until_ts DOUBLE PRECISION NOT NULL)",
    "CREATE TABLE IF NOT EXISTS rate_events (key TEXT NOT NULL, ts DOUBLE PRECISION NOT NULL)",
    "CREATE INDEX IF NOT EXISTS idx_rate_key ON rate_events(key, ts)",
    "CREATE TABLE IF NOT EXISTS lock_levels (key TEXT PRIMARY KEY, level INTEGER NOT NULL, ts DOUBLE PRECISION NOT NULL)",
    "CREATE TABLE IF NOT EXISTS challenges (cid TEXT PRIMARY KEY, ch BYTEA NOT NULL, purpose TEXT NOT NULL, "
    "user_key TEXT NOT NULL, exp DOUBLE PRECISION NOT NULL)",
    "CREATE TABLE IF NOT EXISTS security_log (id BIGSERIAL PRIMARY KEY, ts DOUBLE PRECISION NOT NULL, event TEXT NOT NULL, "
    "user_key TEXT, ip TEXT, detail TEXT)",
    "CREATE INDEX IF NOT EXISTS idx_seclog_ts ON security_log(ts)",
]


def init_db():
    if psycopg is None or not database_url():
        raise RuntimeError("PostgreSQL driver or DATABASE_URL missing")
    with _lock:
        c = db_conn()
        if not SKIP_DDL:
            for stmt in SCHEMA:
                c.execute(stmt)
            c.commit()
        c.execute("INSERT INTO meta(key,value) VALUES('state',?) ON CONFLICT(key) DO NOTHING",
                  (json.dumps(empty_state(), ensure_ascii=False),))
        c.execute("INSERT INTO meta(key,value) VALUES('csrf_secret',?) ON CONFLICT(key) DO NOTHING",
                  (secrets.token_hex(32),))
        c.commit()
        row = c.execute("SELECT value FROM meta WHERE key='state'").fetchone()
        st = json.loads(row["value"])
        users = [u for u in (st.get("users") or {}).values() if isinstance(u, dict)]
        plain = [u for u in users if u.get("password")]
        raw_sessions = [r["token"] for r in c.execute("SELECT token FROM sessions").fetchall()
                        if not re.fullmatch(r"[0-9a-f]{64}", r["token"])]
        dirty = False
        for u in users:
            for f in ("fp", "fp_on"):
                if f in u:
                    u.pop(f, None)
                    dirty = True
        if plain and (ARGON2 or ALLOW_PBKDF2_FALLBACK):
            for u in plain:
                u["pw"] = hash_pw(str(u["password"])[:PW_MAX * 4])
                u.pop("password", None)
                u.pop("salt", None)
                dirty = True
        if dirty:
            c.execute("UPDATE meta SET value=? WHERE key='state'", (json.dumps(st, ensure_ascii=False),))
        for t in raw_sessions:
            c.execute("UPDATE sessions SET token=? WHERE token=?", (token_hash(t), t))
        now = time.time()
        c.execute("DELETE FROM sessions WHERE created<?", (now - SESSION_TTL,))
        c.execute("DELETE FROM locks WHERE until_ts<?", (now,))
        c.execute("DELETE FROM lock_levels WHERE ts<?", (now - LEVEL_DECAY,))
        c.execute("DELETE FROM challenges WHERE exp<?", (now,))
        c.execute("DELETE FROM rate_events WHERE ts<?", (now - RATE_WINDOW,))
        c.execute("DELETE FROM security_log WHERE ts<?", (now - LOG_RETENTION,))
        c.commit()
        sec = c.execute("SELECT value FROM meta WHERE key='csrf_secret'").fetchone()["value"]
        _CSRF_SECRET["k"] = bytes.fromhex(sec)
        c.close()


def audit_passwords():
    st = get_state()
    out = {"argon2id": 0, "pbkdf2": 0, "sha256_legacy": 0, "plaintext": 0, "no_password": 0, "needs_rehash": 0}
    for u in (st.get("users") or {}).values():
        if not isinstance(u, dict):
            continue
        pw = u.get("pw") or ""
        if pw.startswith("$argon2id$"):
            out["argon2id"] += 1
            if ARGON2 and _ph.check_needs_rehash(pw):
                out["needs_rehash"] += 1
        elif pw.startswith("pbkdf2"):
            out["pbkdf2"] += 1
        elif pw:
            out["sha256_legacy"] += 1
        elif u.get("password"):
            out["plaintext"] += 1
        else:
            out["no_password"] += 1
    return out


def get_state():
    with _lock:
        c = db_conn()
        row = c.execute("SELECT value FROM meta WHERE key='state'").fetchone()
        c.close()
        return json.loads(row["value"]) if row else empty_state()


def set_state(state):
    with _lock:
        c = db_conn()
        c.execute(
            "INSERT INTO meta(key,value) VALUES('state',?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (json.dumps(state, ensure_ascii=False),),
        )
        c.commit()
        c.close()


def cred_ids():
    with _lock:
        c = db_conn()
        rows = c.execute("SELECT user_key,cred_id FROM webauthn_creds").fetchall()
        c.close()
    out = {}
    for r in rows:
        out.setdefault(r["user_key"], r["cred_id"])
    return out


def user_creds(user_key):
    with _lock:
        c = db_conn()
        rows = c.execute("SELECT * FROM webauthn_creds WHERE user_key=?", (user_key,)).fetchall()
        c.close()
    return [dict(r) for r in rows]


def public_user(u, uk, creds=None):
    if creds is None:
        creds = cred_ids()
    v = {a: b for a, b in (u or {}).items() if a not in SECRET_USER_FIELDS}
    cid = creds.get(uk, "")
    v["fp"] = cid
    v["fp_on"] = bool(cid)
    return v


def public_state(st):
    out = dict(st)
    out["rev"] = int(_num(st.get("rev")))
    out["snap"] = int(time.time() * 1000)
    creds = cred_ids()
    users = {}
    for k, u in (st.get("users") or {}).items():
        users[k] = public_user(u, k, creds) if isinstance(u, dict) else u
    out["users"] = users
    return out


def anonymous_state():
    st = get_state()
    out = empty_state()
    out["settings"] = st.get("settings") or dict(EMPTY_SETTINGS)
    return out


def merge_state(old, new, uk, admin, notes=None):
    notes = notes if notes is not None else []
    out = dict(new)
    old_users = old.get("users") or {}
    new_users = new.get("users") or {}
    users = {}
    taken = {}
    for k, ou in old_users.items():
        if isinstance(ou, dict):
            taken[(ou.get("first"), ou.get("last"))] = k
    for k, ou in old_users.items():
        if k not in new_users:
            if admin and k != uk:
                continue
            users[k] = ou
            continue
        nu = new_users[k]
        if not isinstance(ou, dict) or not isinstance(nu, dict):
            users[k] = ou
            continue
        base = dict(ou)
        if any(f in nu for f in ("pw", "salt", "pw2", "pass", "password")):
            notes.append("secret_change")
        if "role" in nu and nu.get("role") != ou.get("role"):
            notes.append("role_change")
        if admin:
            for a, b in nu.items():
                if a not in SECRET_USER_FIELDS and a != "role":
                    base[a] = b
        elif k == uk:
            for a in ("first", "last", "avatar"):
                if a in nu and isinstance(nu[a], str) and len(nu[a]) < 2_000_000:
                    base[a] = nu[a]
            owner = taken.get((base.get("first"), base.get("last")))
            if owner not in (None, k):
                base["first"], base["last"] = ou.get("first"), ou.get("last")
        for f in ("fp", "fp_on"):
            base.pop(f, None)
        for f in ("pw", "salt", "pw2", "pass", "password"):
            if f in ou:
                base[f] = ou[f]
            else:
                base.pop(f, None)
        if "role" in ou:
            base["role"] = ou["role"]
        else:
            base.pop("role", None)
        users[k] = base
    out["users"] = users
    if not admin:
        harden_state(old, new, out, uk, notes)
    removed = [k for k in old_users if k not in users]
    return out, removed


def _scrub_surrogates(x):
    if isinstance(x, str):
        return x.encode("utf-8", "replace").decode("utf-8")
    if isinstance(x, list):
        return [_scrub_surrogates(v) for v in x]
    if isinstance(x, dict):
        return {_scrub_surrogates(k): _scrub_surrogates(v) for k, v in x.items()}
    return x


def state_problem(db):
    if not isinstance(db, dict) or db.get("v") != 3:
        return "state"
    for k, t in (("users", dict), ("data", dict), ("orders", list), ("tickets", list), ("pays", list)):
        if k in db and not isinstance(db[k], t):
            return k
    for k in ("tid", "oid", "payc"):
        if k in db and (not isinstance(db[k], int) or isinstance(db[k], bool) or abs(db[k]) > 10 ** 12):
            return k
    if "settings" in db and not isinstance(db["settings"], dict):
        return "settings"
    if "products" in db and db["products"] is not None and not isinstance(db["products"], list):
        return "products"
    stack, nodes = [(db, 0)], 0
    while stack:
        x, depth = stack.pop()
        nodes += 1
        if nodes > 1_500_000 or depth > 14:
            return "too big or too deep"
        if isinstance(x, dict):
            if len(x) > 200_000:
                return "dict too large"
            for k, v in x.items():
                if not isinstance(k, str) or len(k) > 200:
                    return "bad key"
                stack.append((v, depth + 1))
        elif isinstance(x, list):
            if len(x) > 200_000:
                return "list too large"
            stack.extend((v, depth + 1) for v in x)
        elif isinstance(x, str):
            if len(x) > 3_500_000:
                return "string too long"
        elif not (x is None or isinstance(x, (bool, int, float))):
            return "bad type"
        elif isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
            return "bad number"
    return None


def _num(v, default=0):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else default


def _ev_key(x):
    return (x.get("ts"), x.get("t")) if isinstance(x, dict) else None


def merge_events(old_list, new_list, snap):
    new_list = [x for x in (new_list or []) if isinstance(x, dict)]
    old_list = [x for x in (old_list or []) if isinstance(x, dict)]
    have = {_ev_key(x) for x in new_list}
    extra = [x for x in old_list if _ev_key(x) not in have and _num(x.get("ts")) > snap]
    out = new_list + extra
    try:
        out.sort(key=lambda x: -_num(x.get("ts")))
    except Exception:
        pass
    return out[:1000]


_META_KEYS = ("_v", "_bv", "_h", "_bb", "_by")


def _strip_v(x):
    return {k: v for k, v in x.items() if k not in _META_KEYS}


def _hash_item(x):
    return hashlib.sha1(json.dumps(_strip_v(x), sort_keys=True, ensure_ascii=False).encode("utf-8", "replace")).hexdigest()[:12]


def _edited(client_item, server_item):
    if "_h" in client_item:
        return _hash_item(client_item) != client_item["_h"]
    return _strip_v(client_item) != _strip_v(server_item)


def _merge_ticket(o, x, admin=False, snap=0, uk=None):
    if admin:
        old_m = [m for m in (o.get("m") or []) if isinstance(m, dict)]
        new_m = [m for m in (x.get("m") or []) if isinstance(m, dict)]
        new_a = [m for m in new_m if m.get("f") == "a"]
        a_ts = {m.get("ts") for m in new_a}
        keep = [m for m in old_m if m.get("f") != "a"]
        keep_keys = {(m.get("f"), m.get("ts")) for m in keep}
        newer = [m for m in new_m if m.get("f") != "a" and (m.get("f"), m.get("ts")) not in keep_keys]
        other_a = [m for m in old_m if m.get("f") == "a" and m.get("ts") not in a_ts
                   and _num(m.get("ts")) > snap and m.get("by") not in (None, uk)]
        msgs = new_a + keep + newer + other_a
        base = x if _num(x.get("up")) >= _num(o.get("up")) else o
        out = dict(base)
        out["m"] = sorted(msgs, key=lambda m: _num(m.get("ts")))
        return out
    msgs = {}
    for m in list(o.get("m") or []) + list(x.get("m") or []):
        if isinstance(m, dict):
            msgs[(m.get("f"), m.get("ts"), m.get("t"))] = m
    base = x if _num(x.get("up")) >= _num(o.get("up")) else o
    out = dict(base)
    out["m"] = sorted(msgs.values(), key=lambda m: _num(m.get("ts")))
    return out


def _versioned(o, x, conflicts, label, uk=None):
    x = dict(x)
    mine = uk is not None and o.get("_by") == uk
    if _edited(x, o):
        if (not mine) and _num(x.get("_v")) < _num(o.get("_v")) and _strip_v(x) != _strip_v(o):
            conflicts.append(label)
            x = dict(o)
    else:
        x = dict(o)
    changed = _strip_v(x) != _strip_v(o)
    x["_v"] = _num(o.get("_v")) + (1 if changed else 0)
    if changed and uk is not None:
        x["_by"] = uk
    elif "_by" in o:
        x["_by"] = o["_by"]
    else:
        x.pop("_by", None)
    x["_h"] = _hash_item(x)
    return x


def finalize_state(old, new_db, merged, admin, uk, conflicts, audits=None):
    audits = audits if audits is not None else []
    stale = new_db.get("rev") != old.get("rev", 0)
    snap = _num(new_db.get("snap"))
    for key, ctr in (("orders", "oid"), ("pays", "payc"), ("tickets", "tid"), ("products", None)):
        mer = merged.get(key)
        if not isinstance(old.get(key), list) or not isinstance(mer, list):
            continue
        old_l = [x for x in old[key] if isinstance(x, dict)]
        old_by = {x.get("id"): x for x in old_l}
        out, seen = [], set()
        for x in mer:
            if not isinstance(x, dict):
                out.append(x)
                continue
            o = old_by.get(x.get("id"))
            seen.add(x.get("id"))
            if o is None:
                x = dict(x)
                x["_v"] = 0
                x["_by"] = uk
                x["_h"] = _hash_item(x)
                out.append(x)
                continue
            if key == "tickets":
                x = _merge_ticket(o, x, admin, snap, uk)
                x = dict(x)
                x["_v"] = _num(o.get("_v")) + (1 if _strip_v(x) != _strip_v(o) else 0)
                x["_h"] = _hash_item(x)
                out.append(x)
            else:
                nx = _versioned(o, x, conflicts, "%s:%s" % (key, x.get("id")), uk)
                if key == "products" and admin and nx.get("_v") != o.get("_v"):
                    audits.append(("catalog_change", {"product": str(x.get("id"))[:40]}))
                out.append(nx)
        if admin and ctr:
            floor = _num((new_db.get("_fl") or {}).get(ctr, new_db.get(ctr)))
            out += [o for o in old_l if o.get("id") not in seen and _num(o.get("id")) > floor]
        if key in ("orders", "pays", "tickets"):
            try:
                out.sort(key=lambda x: -_num(x.get("id")))
            except Exception:
                pass
        merged[key] = out
    ou, mu = old.get("users") or {}, merged.get("users") or {}
    for k, m in list(mu.items()):
        o = ou.get(k)
        if isinstance(m, dict) and isinstance(o, dict):
            mu[k] = _versioned(o, m, conflicts, "user:%s" % k, uk)
    od, md, nd = old.get("data") or {}, merged.get("data") or {}, new_db.get("data") or {}
    for k, m in list(md.items()):
        o = od.get(k)
        if not isinstance(m, dict) or not isinstance(o, dict):
            continue
        m = dict(m)
        if admin or k == uk:
            for ev in ("tx", "notif"):
                m[ev] = merge_events(o.get(ev), m.get(ev), snap)
        cl = nd.get(k) if isinstance(nd.get(k), dict) else {}
        server_bal = o.get("bal", 0)
        if admin:
            edited = _num(m.get("bal")) != _num(cl.get("_bb", server_bal))
            if not edited:
                m["bal"] = server_bal
            elif _num(m.get("bal")) != _num(server_bal) and _num(cl.get("_bv")) < _num(o.get("_bv")) and o.get("_bu") != uk:
                conflicts.append("bal:%s" % k)
                m["bal"] = server_bal
        if _num(m.get("bal")) != _num(server_bal):
            if admin:
                audits.append(("balance_change", {"user": k, "from": server_bal, "to": m.get("bal")}))
            m["_bv"] = _num(o.get("_bv")) + 1
            m["_bu"] = uk
        else:
            m["_bv"] = _num(o.get("_bv"))
            if "_bu" in o:
                m["_bu"] = o["_bu"]
            else:
                m.pop("_bu", None)
        m["_bb"] = m.get("bal", 0)
        md[k] = m
    merged["rev"] = int(_num(old.get("rev"))) + 1
    merged.pop("snap", None)
    merged.pop("_fl", None)
    return stale


def renumber_new(old, new_db, notes):
    """اگر شمارهٔ سفارش/پرداخت/تیکت جدیدِ کلاینت با مورد دیگری تصادم کرد، شمارهٔ تازه می‌گیرد."""
    fresh = {"orders": set(), "pays": set()}
    maps = {}
    for key, ctr in (("orders", "oid"), ("pays", "payc"), ("tickets", "tid")):
        nl = new_db.get(key)
        if not isinstance(nl, list):
            continue
        ol = [x for x in (old.get(key) or []) if isinstance(x, dict)]
        old_by = {x.get("id"): x for x in ol}
        ids = [_num(old.get(ctr))] + [_num(x.get("id")) for x in ol] + \
              [_num(x.get("id")) for x in nl if isinstance(x, dict)]
        top = max(ids + [0])
        mp = {}
        for x in nl:
            if not isinstance(x, dict):
                continue
            o = old_by.get(x.get("id"))
            if o is None:
                if key in fresh:
                    fresh[key].add(id(x))
                continue
            if o.get("u") != x.get("u") or o.get("ts") != x.get("ts"):
                top += 1
                mp[x.get("id")] = top
                x["id"] = top
                if key in fresh:
                    fresh[key].add(id(x))
        if mp:
            maps[key] = mp
            notes.append("renumbered")
        new_db[ctr] = int(max(_num(new_db.get(ctr)), top if mp else 0))
    for x in new_db.get("orders") or []:
        if isinstance(x, dict) and id(x) in fresh["orders"] and x.get("pay") in maps.get("pays", {}):
            x["pay"] = maps["pays"][x["pay"]]
    for p in new_db.get("pays") or []:
        if isinstance(p, dict) and id(p) in fresh["pays"] and p.get("oid") in maps.get("orders", {}):
            p["oid"] = maps["orders"][p["oid"]]


def conflict_messages(conflicts):
    out = []
    for c in conflicts:
        kind, _, ident = c.partition(":")
        n = _fa(ident) if ident.isdigit() else ""
        if kind == "orders":
            out.append("سفارش #%s هم‌زمان توسط شخص دیگری تغییر کرده بود؛ تغییر شما ثبت نشد و نسخهٔ جدید نمایش داده شد." % n)
        elif kind == "pays":
            out.append("درخواست پرداخت #%s هم‌زمان توسط شخص دیگری تغییر کرده بود؛ تغییر شما ثبت نشد و نسخهٔ جدید نمایش داده شد." % n)
        elif kind == "products":
            out.append("یک محصول هم‌زمان توسط شخص دیگری ویرایش شده بود؛ تغییر شما ثبت نشد و نسخهٔ جدید نمایش داده شد.")
        elif kind == "user":
            out.append("اطلاعات یک کاربر هم‌زمان تغییر کرده بود؛ تغییر شما ثبت نشد.")
        elif kind == "bal":
            out.append("موجودی یک کاربر هم‌زمان تغییر کرده بود؛ تغییر شما ثبت نشد. مقدار فعلی را بررسی و در صورت نیاز دوباره اعمال کن.")
        else:
            out.append("تغییر شما هم‌زمان با تغییر دیگری بود و ثبت نشد.")
    return out


def catalog_price(catalog, o):
    try:
        p = next(x for x in catalog if x.get("id") == o.get("pid"))
        t = next(x for x in p["types"] if x.get("id") == o.get("tid"))
        it = next(x for x in t["items"] if x.get("id") == o.get("iid"))
        q = o.get("qty")
        if isinstance(q, bool) or not isinstance(q, (int, float)) or q != int(q) or q < it["min"] or q > it["max"]:
            return None
        return max(100, math.floor(it["rate"] * q / 1000 + 0.5))
    except Exception:
        return None


def harden_state(old, new, out, uk, notes=None):
    notes = notes if notes is not None else []
    for key in ("settings", "products"):
        if key in old:
            out[key] = old[key]
        else:
            out.pop(key, None)
    od, nd = old.get("data") or {}, new.get("data") or {}
    data = {}
    for k, ov in od.items():
        nv = nd.get(k)
        if not isinstance(ov, dict) or not isinstance(nv, dict):
            data[k] = ov
        elif k == uk:
            v = dict(nv)
            v["bal"] = ov.get("bal", 0)
            data[k] = v
        else:
            v = dict(ov)
            if isinstance(nv.get("notif"), list):
                have = {_ev_key(x) for x in (ov.get("notif") or [])}
                fresh_n = [x for x in nv["notif"] if isinstance(x, dict) and _ev_key(x) not in have]
                v["notif"] = (fresh_n + list(ov.get("notif") or []))[:300]
            data[k] = v
    out["data"] = data
    catalog = old.get("products") if isinstance(old.get("products"), list) else None
    old_orders = [x for x in (old.get("orders") or []) if isinstance(x, dict)]
    old_pays = [x for x in (old.get("pays") or []) if isinstance(x, dict)]
    oo_ids = {x.get("id") for x in old_orders}
    op_by = {x.get("id"): x for x in old_pays}
    oo_by = {x.get("id"): x for x in old_orders}

    if "pays" in new:
        pays = []
        for x in (new.get("pays") or []):
            if not isinstance(x, dict) or x.get("u") != uk:
                continue
            prev = op_by.get(x.get("id"))
            x = dict(x)
            if prev is not None:
                if prev.get("u") != uk:
                    continue
                if x.get("s") != prev.get("s") and x.get("s") in ("ok", "rejected"):
                    notes.append("pay_forged")
                for f in ("s", "cr", "note", "amt", "kind", "oid", "u"):
                    if f in prev:
                        x[f] = prev[f]
                    else:
                        x.pop(f, None)
            else:
                if x.get("s") != "pending" or "cr" in x:
                    notes.append("pay_forged")
                x["s"] = "pending"
                x.pop("cr", None)
                if not isinstance(x.get("id"), int) or isinstance(x.get("id"), bool) or x["id"] in op_by:
                    continue
            pays.append(x)
    else:
        pays = []
    seen_p = {x.get("id") for x in pays}
    pays += [x for x in old_pays if x.get("id") not in seen_p]

    orders = []
    fresh = []
    if "orders" in new:
        for x in (new.get("orders") or []):
            if not isinstance(x, dict):
                continue
            prev = oo_by.get(x.get("id"))
            if prev is not None:
                if prev.get("u") == uk:
                    x = dict(x)
                    for f in ("st", "rf", "dn", "price", "note", "qty", "pid", "tid", "iid", "u", "pay"):
                        if f in prev:
                            x[f] = prev[f]
                        else:
                            x.pop(f, None)
                    orders.append(x)
                continue
            if x.get("u") != uk:
                notes.append("forged_owner")
                continue
            fresh.append(dict(x))
    old_bal = _num((od.get(uk) or {}).get("bal"))
    spent = 0
    pays_by_id = {x.get("id"): x for x in pays}
    taken_ids = set(oo_ids)
    for x in sorted(fresh, key=lambda o: _num(o.get("id"))):
        pr = _num(x.get("price"), None)
        oid = x.get("id")
        if pr is None or pr < 100 or isinstance(oid, bool) or not isinstance(oid, int) or oid in taken_ids:
            notes.append("order_rejected")
            continue
        if catalog is not None and catalog_price(catalog, x) != pr:
            notes.append("price_mismatch")
            continue
        x["rf"], x["dn"] = 0, 0
        pay_id = x.get("pay")
        if pay_id:
            p = pays_by_id.get(pay_id)
            if not p or p.get("u") != uk or p.get("kind") != "order" or p.get("oid") != oid or _num(p.get("amt"), None) != pr:
                notes.append("order_rejected")
                continue
            x["st"] = "proc"
        else:
            if spent + pr > old_bal:
                notes.append("order_rejected")
                continue
            spent += pr
            x["st"] = "queue"
        taken_ids.add(oid)
        orders.append(x)
    od_uk = out["data"].get(uk)
    if isinstance(od_uk, dict):
        od_uk["bal"] = old_bal - spent
        if "tx" not in od_uk or not isinstance(od_uk.get("tx"), list):
            od_uk["tx"] = (od.get(uk) or {}).get("tx", [])
    kept = {x.get("id") for x in orders}
    seen_o = set(kept)
    orders += [x for x in old_orders if x.get("id") not in seen_o]
    live_orders = {x.get("id") for x in orders}
    pays = [p for p in pays if not (p.get("kind") == "order" and p.get("oid") not in live_orders)]
    for lst, key in ((orders, "orders"), (pays, "pays")):
        try:
            lst.sort(key=lambda x: -_num(x.get("id")))
        except Exception:
            pass
    out["orders"], out["pays"] = orders, pays

    if "tickets" in new:
        olds = [x for x in (old.get("tickets") or []) if isinstance(x, dict)]
        old_t = {x.get("id"): x for x in olds}
        mine = []
        for x in (new.get("tickets") or []):
            if not isinstance(x, dict) or x.get("u") != uk:
                continue
            o = old_t.get(x.get("id"))
            if o is not None and o.get("u") != uk:
                continue
            if o is not None and o.get("s") == "closed":
                keep = dict(o)
                ur = dict(o.get("ur") or {})
                if isinstance(x.get("ur"), dict) and not x["ur"].get("u"):
                    ur["u"] = 0
                keep["ur"] = ur
                mine.append(keep)
                continue
            mine.append(x)
        seen = {x.get("id") for x in mine}
        tk = mine + [x for x in olds if x.get("id") not in seen]
        try:
            tk.sort(key=lambda x: -_num(x.get("id")))
        except Exception:
            pass
        out["tickets"] = tk
    else:
        out["tickets"] = old.get("tickets", [])
    for ctr in ("oid", "tid", "payc"):
        out[ctr] = max(_num(old.get(ctr)), _num(new.get(ctr)))


def drop_user_auth(user_keys):
    if not user_keys:
        return
    with _lock:
        c = db_conn()
        for k in user_keys:
            c.execute("DELETE FROM webauthn_creds WHERE user_key=?", (k,))
            c.execute("DELETE FROM sessions WHERE user_key=?", (k,))
            c.execute("DELETE FROM devices WHERE user_key=?", (k,))
        c.commit()
        c.close()


def device_user(device_id):
    if not device_id:
        return None
    with _lock:
        c = db_conn()
        row = c.execute("SELECT user_key FROM devices WHERE device_id=?", (device_id,)).fetchone()
        c.close()
        return row["user_key"] if row else None


def bind_device(device_id, user_key):
    if not device_id or not user_key or len(device_id) > 200:
        return
    with _lock:
        c = db_conn()
        c.execute(
            "INSERT INTO devices(device_id,user_key,created) VALUES(?,?,?) "
            "ON CONFLICT(device_id) DO UPDATE SET user_key=excluded.user_key",
            (device_id, user_key, time.time()),
        )
        c.commit()
        c.close()


def make_session(user_key, device_id=None):
    token = secrets.token_urlsafe(32)
    with _lock:
        c = db_conn()
        c.execute(
            "INSERT INTO sessions(token,user_key,device_id,created) VALUES(?,?,?,?)",
            (token_hash(token), user_key, (device_id or "")[:200], time.time()),
        )
        rows = c.execute("SELECT token FROM sessions WHERE user_key=? ORDER BY created DESC", (user_key,)).fetchall()
        for r in rows[MAX_SESSIONS:]:
            c.execute("DELETE FROM sessions WHERE token=?", (r["token"],))
        c.commit()
        c.close()
    return token


def drop_all_sessions(user_key):
    with _lock:
        c = db_conn()
        c.execute("DELETE FROM sessions WHERE user_key=?", (user_key,))
        c.commit()
        c.close()


def rotate_session(token):
    new = secrets.token_urlsafe(32)
    with _lock:
        c = db_conn()
        c.execute("UPDATE sessions SET token=? WHERE token=?", (token_hash(new), token_hash(token)))
        c.commit()
        c.close()
    return new


def drop_session(token):
    if token:
        with _lock:
            c = db_conn()
            c.execute("DELETE FROM sessions WHERE token=?", (token_hash(token),))
            c.commit()
            c.close()


def session_user(token):
    if not token or len(token) > 200:
        return None
    with _lock:
        c = db_conn()
        row = c.execute("SELECT user_key,created FROM sessions WHERE token=?", (token_hash(token),)).fetchone()
        c.close()
    if not row or row["created"] < time.time() - SESSION_TTL:
        return None
    return row["user_key"]


class Handler(BaseHTTPRequestHandler):
    server_version = "Arka"
    sys_version = ""
    timeout = SOCKET_TIMEOUT
    protocol_version = "HTTP/1.0"

    def log_message(self, fmt, *args):
        try:
            sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))
            sys.stdout.flush()
        except Exception:
            pass

    def _is_https(self):
        if isinstance(self.connection, ssl.SSLSocket):
            return True
        if COOKIE_SECURE:
            return True
        return TRUST_PROXY and \
            (self.headers.get("X-Forwarded-Proto") or "").lower() == "https"

    def _cookie_header(self, token, clear=False):
        parts = ["%s=%s" % (COOKIE_NAME, "" if clear else token), "Path=/", "HttpOnly", "SameSite=Strict",
                 "Max-Age=%d" % (0 if clear else SESSION_TTL)]
        if self._is_https() or PRODUCTION:
            parts.append("Secure")
        return "; ".join(parts)

    def _token(self):
        self._tok_src = ""
        t = self.headers.get("X-Token") or ""
        if t and token_header_allowed():
            self._tok_src = "header"
            return t
        raw = self.headers.get("Cookie") or ""
        try:
            jar = http.cookies.SimpleCookie()
            jar.load(raw)
            if COOKIE_NAME in jar:
                self._tok_src = "cookie"
                return jar[COOKIE_NAME].value
        except Exception:
            pass
        return ""

    def _sec_headers(self, nonce=None):
        https = self._is_https()
        if https:
            self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy",
                         "camera=(), microphone=(), geolocation=(), payment=(), usb=(), "
                         "publickey-credentials-get=(self), publickey-credentials-create=(self)")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Permitted-Cross-Domain-Policies", "none")
        if nonce:
            csp = ("default-src 'self'; script-src 'self' 'nonce-%s'; "
                   "style-src 'self' 'unsafe-inline'; "
                   "font-src 'self'; img-src 'self' data: blob:; "
                   "media-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'; "
                   "base-uri 'self'; object-src 'none'; form-action 'self'" % nonce)
            if https:
                csp += "; upgrade-insecure-requests"
        else:
            csp = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        self.send_header("Content-Security-Policy", csp)

    def _locked(self, secs):
        mins = max(1, (int(secs) + 59) // 60)
        return self._json(429, {"detail": "تلاش‌های ناموفق زیاد است؛ حدود %d دقیقه دیگر دوباره امتحان کن." % mins,
                                "retry": int(secs)}, extra={"Retry-After": str(int(secs))})

    def _json(self, code, obj, cookie=None, extra=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self._sec_headers()
        self.end_headers()
        self.wfile.write(body)

    def _html(self, code, text):
        nonce = secrets.token_urlsafe(16)
        text = text.replace("<script>", '<script nonce="%s">' % nonce)
        body = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self._sec_headers(nonce)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self, limit=MAX_BODY):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None
        if n <= 0:
            return {}
        if n > limit:
            return None
        raw = self.rfile.read(n)
        try:
            d = json.loads(raw.decode("utf-8"))
            if re.search(rb"\\u[dD][89a-fA-F]", raw):
                d = _scrub_surrogates(d)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}

    def _ip(self):
        if TRUST_PROXY:
            xf = (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
            if xf:
                return xf
        return self.client_address[0]

    def _auth(self):
        return session_user(self._token())

    def _backup_auth(self, uk, data, ip):
        """اثر انگشت یا رمز مدیر. اگر موفق بود mode را برمی‌گرداند؛ وگرنه خودش پاسخ خطا می‌فرستد و None برمی‌گرداند."""
        st = get_state()
        u = (st.get("users") or {}).get(uk) or {}
        creds = user_creds(uk)
        if creds:
            try:
                ch = take_challenge(data.get("cid"), "backup", uk)
                cred = next((c for c in creds if c["cred_id"] == data.get("id")), None)
                if not cred:
                    raise WebAuthnError("unknown credential")
                counter = verify_assertion(expected_rp_id(self), ch, cred, data)
                with _lock:
                    c = db_conn()
                    c.execute("UPDATE webauthn_creds SET sign_count=? WHERE cred_id=?", (counter, cred["cred_id"]))
                    c.commit()
                    c.close()
                return "webauthn"
            except WebAuthnError:
                log_event("backup_fp_fail", uk, ip)
                self._json(400, {"detail": "تأیید اثر انگشت ناموفق بود."})
                return None
        raw_pw = data.get("password") if isinstance(data.get("password"), str) else ""
        if not raw_pw or len(raw_pw) > PW_MAX:
            self._json(400, {"detail": "رمز عبور را وارد کنید."})
            return None
        ok, _ = check_pw(u, raw_pw)
        if not ok:
            log_event("backup_pw_fail", uk, ip)
            rate_fail("backup:" + ip)
            self._json(400, {"detail": "رمز عبور نادرست است."})
            return None
        return "password"

    def _is_admin(self, uk, st=None):
        st = st or get_state()
        u = (st.get("users") or {}).get(uk)
        return bool(isinstance(u, dict) and u.get("role") == "admin")

    def _login_reply(self, uk, device, st=None):
        st = st or get_state()
        if device:
            bind_device(device, uk)
        tok = make_session(uk, device)
        pst = public_state(st)
        return self._json(200, {"token": tok, "csrf": csrf_for(tok), "user": pst["users"][uk], "user_key": uk, "db": pst},
                          cookie=self._cookie_header(tok))

    def _host_ok(self):
        host = (self.headers.get("Host") or "").split(":")[0].strip().lower()
        if ALLOWED_HOSTS:
            return host in ALLOWED_HOSTS or (not PRODUCTION and host in ("localhost", "127.0.0.1"))
        return not PRODUCTION

    def _method_not_allowed(self):
        return self._json(405, {"detail": "method not allowed"}, extra={"Allow": "GET, POST, OPTIONS"})

    do_PUT = do_DELETE = do_PATCH = do_HEAD = _method_not_allowed

    def _force_https(self):
        if PRODUCTION and not self._is_https():
            loop = self.client_address[0] in ("127.0.0.1", "::1") and not self.headers.get("X-Forwarded-For") \
                and not self.headers.get("X-Forwarded-Proto")
            if loop and urlparse(self.path).path == "/api/health":
                return False
            if self.command != "GET":
                self._json(426, {"detail": "HTTPS required"})
                return True
            host = (self.headers.get("Host") or "").split(":")[0]
            self.send_response(308)
            self.send_header("Location", "https://%s%s" % (host, self.path))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return True
        return False

    def do_OPTIONS(self):
        self.send_response(204)
        self._sec_headers()
        self.end_headers()

    def do_GET(self):
        try:
            if not self._host_ok():
                return self._json(400, {"detail": "host not allowed"})
            if self._force_https():
                return
            self._get()
        except Exception as e:
            sys.stderr.write("server error: %s\n" % type(e).__name__)
            try:
                self._json(500, {"detail": "خطای سرور"})
            except Exception:
                pass
        finally:
            release_thread_conns()

    def _get(self):
        path = urlparse(self.path).path
        if path in ("/logo.jpg", "/logo.jpeg", "/favicon.ico"):
            body = LOGO_JPEG
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self._sec_headers()
            self.end_headers()
            self.wfile.write(body)
            return
        if path in ("/", "/index.html", "/arka.html", "/app"):
            host = (self.headers.get("Host") or "")
            hn = host.split(":")[0]
            if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", hn) and hn.startswith("127."):
                port = host.split(":")[1] if ":" in host else str(PORT)
                self.send_response(302)
                self.send_header("Location", "http://localhost:%s%s" % (port, path))
                self.end_headers()
                return
            return self._html(200, HTML_PAGE)
        if path == "/fonts.css":
            body = font_css().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=300")
            self._sec_headers()
            self.end_headers()
            self.wfile.write(body)
            return
        if path.startswith("/fonts/"):
            name = urllib.parse.unquote(path[len("/fonts/"):])
            if name not in font_files():
                return self._json(404, {"detail": "not found"})
            with open(os.path.join(FONT_DIR, name), "rb") as fh:
                body = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", "font/woff2")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self._sec_headers()
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/health":
            return self._json(200, {"ok": True})
        if path == "/api/state":
            uk = self._auth()
            if not uk:
                return self._json(401, {"detail": "وارد حساب شو."})
            return self._json(200, {"db": public_state(get_state()), "user_key": uk, "csrf": csrf_for(self._token())})
        return self._json(404, {"detail": "not found"})

    def do_POST(self):
        try:
            if not self._host_ok():
                return self._json(400, {"detail": "host not allowed"})
            if self._force_https():
                return
            self._post()
        except WebAuthnError:
            self._json(400, {"detail": "تأیید اثر انگشت ناموفق بود."})
        except Exception as e:
            sys.stderr.write("server error: %s\n" % type(e).__name__)
            try:
                self._json(500, {"detail": "خطای سرور"})
            except Exception:
                pass
        finally:
            release_thread_conns()

    def _post(self):
        path = urlparse(self.path).path
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).netloc.lower() != (self.headers.get("Host") or "").lower():
            log_event("origin_block", None, self._ip(), {"origin": origin[:100]})
            return self._json(403, {"detail": "درخواست نامعتبر."})
        data = self._read_json(MAX_BODY if path in ("/api/state", "/api/backup/restore") else SMALL_BODY)
        if data is None:
            return self._json(413, {"detail": "درخواست نامعتبر یا خیلی بزرگ است."})
        device = (self.headers.get("X-Device") or data.get("device") or "")
        device = device if isinstance(device, str) else ""
        token = self._token()
        ip = self._ip()
        if path in CSRF_PATHS and token and self._tok_src == "cookie":
            if not hmac.compare_digest(self.headers.get("X-CSRF") or "", csrf_for(token)):
                log_event("csrf_block", None, ip, {"path": path})
                return self._json(403, {"detail": "درخواست نامعتبر."})

        if path == "/api/logout":
            drop_session(token)
            return self._json(200, {"ok": True}, cookie=self._cookie_header("", clear=True))

        if path == "/api/logout-all":
            uk = session_user(token)
            if not uk:
                return self._json(401, {"detail": "وارد حساب شو."})
            drop_all_sessions(uk)
            log_event("logout_all", uk, ip)
            return self._json(200, {"ok": True}, cookie=self._cookie_header("", clear=True))

        if path == "/api/state":
            uk = session_user(token)
            if not uk:
                return self._json(401, {"detail": "وارد حساب شو."})
            new_db = data.get("db")
            problem = state_problem(new_db)
            if problem:
                log_event("state_rejected", uk, ip, {"why": problem})
                return self._json(400, {"detail": "state نامعتبر"})
            notes = []
            conflicts = []
            audits = []
            with _lock:
                old = get_state()
                is_admin = self._is_admin(uk, old)
                new_db["_fl"] = {c: int(_num(new_db.get(c))) for c in ("oid", "payc", "tid")}
                renumber_new(old, new_db, notes)
                merged, removed = merge_state(old, new_db, uk, is_admin, notes)
                stale = finalize_state(old, new_db, merged, is_admin, uk, conflicts, audits)
                set_state(merged)
            for ev, det in audits[:50]:
                log_event(ev, uk, ip, det)
            drop_user_auth(removed)
            if conflicts:
                log_event("state_conflict", uk, ip, {"items": conflicts[:20]})
            mybal = ((merged.get("data") or {}).get(uk) or {}).get("bal")
            sent = ((new_db.get("data") or {}).get(uk) or {}).get("bal")
            adopt = bool(stale or conflicts or notes or mybal != sent)
            TAMPER = ("secret_change", "role_change", "pay_forged", "forged_owner", "price_mismatch")
            hit = sorted({n for n in notes if n in TAMPER})
            if hit:
                log_event("state_tamper", uk, ip, {"what": hit})
            elif notes:
                log_event("state_adjusted", uk, ip, {"what": sorted(set(notes))})
            reply = {"ok": True, "rev": merged.get("rev"), "conflicts": conflicts,
                     "conflict_msgs": conflict_messages(conflicts)}
            if adopt:
                reply["adopt"] = True
                reply["db"] = public_state(merged)
            return self._json(200, reply)

        if path == "/api/reset":
            uk = session_user(token)
            if not uk or not self._is_admin(uk):
                log_event("reset_denied", uk, ip)
                return self._json(403, {"detail": "فقط مدیر می‌تواند این کار را انجام دهد."})
            log_event("db_reset", uk, ip)
            with _lock:
                c = db_conn()
                c.execute("DELETE FROM devices")
                c.execute("DELETE FROM sessions")
                c.execute("DELETE FROM webauthn_creds")
                c.execute("DELETE FROM challenges")
                c.execute("UPDATE meta SET value=? WHERE key='state'", (json.dumps(empty_state(), ensure_ascii=False),))
                c.commit()
                c.close()
            return self._json(200, {"ok": True, "detail": "دیتابیس از صفر شد"})

        if path == "/api/register":
            first = data.get("first_name") or data.get("first") or ""
            last = data.get("last_name") or data.get("last") or ""
            password = data.get("password") if isinstance(data.get("password"), str) else (
                data.get("pass") if isinstance(data.get("pass"), str) else "")
            first = first.strip() if isinstance(first, str) else ""
            last = last.strip() if isinstance(last, str) else ""
            wait = rate_blocked("reg:" + ip, 30)
            if wait:
                return self._locked(wait)
            if not first or not last:
                return self._json(400, {"detail": "نام و نام خانوادگی را کامل وارد کنید."})
            if not name_ok(first) or not name_ok(last):
                return self._json(400, {"detail": "نام نامعتبر است."})
            problem = password_problem(password, first, last)
            if problem:
                return self._json(400, {"detail": problem})
            rate_fail("reg:" + ip)
            try:
                pw_hash = hash_pw(password)
            except RuntimeError:
                return self._json(500, {"detail": "خطای سرور"})
            with _lock:
                st = get_state()
                users = st.setdefault("users", {})
                admin_cand = first == "Arka" and last == "Member"
                if admin_cand and not ALLOW_WEB_ADMIN:
                    return self._json(400, {"detail": "ساخت حساب مدیر از طریق وب مجاز نیست؛ روی سرور از python arka.py --create-admin استفاده کن."})
                if admin_cand:
                    if any(
                        (u or {}).get("role") == "admin"
                        or ((u or {}).get("first") == "Arka" and (u or {}).get("last") == "Member")
                        for u in users.values()
                    ):
                        return self._json(400, {"detail": "حسابی با این نام وجود دارد."})
                else:
                    if re.search(r"[A-Za-z]", first + last):
                        return self._json(400, {"detail": "نام فقط باید با حروف فارسی نوشته شود."})
                    if any((u or {}).get("first") == first and (u or {}).get("last") == last for u in users.values()):
                        return self._json(400, {"detail": "حسابی با این نام وجود دارد."})
                key = "u" + uuid.uuid4().hex[:12]
                rec = {
                    "first": first,
                    "last": last,
                    "email": key,
                    "avatar": "",
                    "uid": str(int(1e7 + (uuid.uuid4().int % 90000000))),
                    "joined": int(time.time() * 1000),
                    "pw": pw_hash,
                }
                if admin_cand:
                    rec["role"] = "admin"
                    log_event("first_admin_created", key, ip, {"how": "web"})
                    log_event("admin_registered", key, ip)
                users[key] = rec
                st.setdefault("data", {})[key] = {"bal": 0, "tx": [], "notif": []}
                set_state(st)
            if device:
                bind_device(device, key)
            tok = make_session(key, device)
            log_event("register", key, ip)
            return self._json(200, {"token": tok, "csrf": csrf_for(tok), "user": public_user(rec, key), "user_key": key},
                              cookie=self._cookie_header(tok))

        if path == "/api/fp":
            uk = session_user(token)
            if not uk:
                return self._json(401, {"detail": "وارد حساب شو."})
            if data.get("enable"):
                return self._json(400, {"detail": "ثبت اثر انگشت باید با تأیید حسگر انجام شود."})
            drop_creds = user_creds(uk)
            if drop_creds:
                with _lock:
                    c = db_conn()
                    c.execute("DELETE FROM webauthn_creds WHERE user_key=?", (uk,))
                    c.commit()
                    c.close()
            st = get_state()
            log_event("fp_disabled", uk, ip)
            if self._is_admin(uk):
                log_event("admin_fp_disabled", uk, ip)
            reply = {"ok": True, "user": public_user(st["users"].get(uk), uk)}
            if self._tok_src == "cookie":
                new_tok = rotate_session(token)
                reply["csrf"] = csrf_for(new_tok)
                return self._json(200, reply, cookie=self._cookie_header(new_tok))
            return self._json(200, reply)

        if path == "/api/fp/register-options":
            uk = session_user(token)
            st = get_state()
            if not uk or uk not in st.get("users", {}):
                return self._json(401, {"detail": "وارد حساب شو."})
            u = st["users"][uk]
            cid, ch = new_challenge("reg", uk)
            return self._json(200, {
                "cid": cid,
                "challenge": b64u_enc(ch),
                "rpId": expected_rp_id(self),
                "user": {
                    "id": b64u_enc(hashlib.sha256(("arka:" + uk).encode()).digest()),
                    "name": uk,
                    "displayName": ((u.get("first") or "") + " " + (u.get("last") or "")).strip() or "Arka",
                },
                "exclude": [c["cred_id"] for c in user_creds(uk)],
            })

        if path == "/api/fp/register":
            uk = session_user(token)
            st = get_state()
            if not uk or uk not in st.get("users", {}):
                return self._json(401, {"detail": "وارد حساب شو."})
            ch = take_challenge(data.get("cid"), "reg", uk)
            cred_id, alg, pub, counter = verify_registration(expected_rp_id(self), ch, data)
            with _lock:
                c = db_conn()
                other = c.execute("SELECT user_key FROM webauthn_creds WHERE cred_id=?", (cred_id,)).fetchone()
                if other and other["user_key"] != uk:
                    c.close()
                    return self._json(400, {"detail": "این اثر انگشت برای حساب دیگری است."})
                c.execute("DELETE FROM webauthn_creds WHERE user_key=?", (uk,))
                c.execute(
                    "INSERT INTO webauthn_creds(cred_id,user_key,alg,pub,sign_count,created) VALUES(?,?,?,?,?,?)",
                    (cred_id, uk, alg, pub, counter, time.time()),
                )
                c.commit()
                c.close()
            log_event("fp_enrolled", uk, ip)
            reply = {"ok": True, "id": cred_id, "user": public_user(st["users"][uk], uk)}
            if self._tok_src == "cookie":
                new_tok = rotate_session(token)
                reply["csrf"] = csrf_for(new_tok)
                return self._json(200, reply, cookie=self._cookie_header(new_tok))
            return self._json(200, reply)

        if path == "/api/lookup":
            if throttled("lk:" + ip, 30):
                return self._locked(60)
            first = str(data.get("first") or "").strip()
            last = str(data.get("last") or "").strip()
            st = get_state()
            creds = cred_ids()
            for k, u in (st.get("users") or {}).items():
                if u and u.get("first") == first and u.get("last") == last:
                    cid = creds.get(k, "")
                    return self._json(200, {"user_key": k, "fp": cid, "fp_on": bool(cid), "has_pw": bool(u.get("pw")),
                                            "lock": lock_remaining("lacct:" + k), "challenge": challenge_for(k, ip)})
            dk = decoy_key(first, last)
            return self._json(200, {"user_key": dk, "fp": "", "fp_on": False, "has_pw": True,
                                    "lock": lock_remaining("lacct:" + dk), "challenge": challenge_for(dk, ip)})

        if path == "/api/fp/options":
            if throttled("fo:" + ip, 30):
                return self._locked(60)
            uk = str(data.get("user_key") or "").strip()
            creds = user_creds(uk) if uk else []
            if not creds:
                return self._json(400, {"detail": "برای این حساب اثر انگشت فعال نشده. با رمز وارد شو."})
            cid, ch = new_challenge("auth", uk)
            return self._json(200, {
                "cid": cid,
                "challenge": b64u_enc(ch),
                "rpId": expected_rp_id(self),
                "allow": [c["cred_id"] for c in creds],
            })

        if path == "/api/fp/login":
            uk = str(data.get("user_key") or "").strip()
            rk_ip, rk_acct = "fpip:" + ip, "fpacct:" + uk
            wait = max(rate_blocked(rk_ip, 40), rate_blocked(rk_acct))
            if wait:
                return self._locked(wait)
            try:
                ch = take_challenge(data.get("cid"), "auth", uk)
                cred = next((c for c in user_creds(uk) if c["cred_id"] == data.get("id")), None)
                if not cred:
                    raise WebAuthnError("unknown credential")
                counter = verify_assertion(expected_rp_id(self), ch, cred, data)
            except WebAuthnError:
                rate_fail(rk_ip)
                rate_fail(rk_acct)
                log_event("fp_login_fail", uk, ip)
                wait = max(rate_blocked(rk_ip, 40), rate_blocked(rk_acct))
                if wait:
                    return self._locked(wait)
                return self._json(400, {"detail": "تأیید اثر انگشت ناموفق بود."})
            with _lock:
                c = db_conn()
                c.execute("UPDATE webauthn_creds SET sign_count=? WHERE cred_id=?", (counter, cred["cred_id"]))
                c.commit()
                c.close()
            rate_ok(rk_acct)
            log_event("fp_login_ok", uk, ip)
            return self._login_reply(uk, device)

        if path == "/api/login":
            uk = data.get("user_key") if isinstance(data.get("user_key"), str) else ""
            raw_pw = data.get("password") if isinstance(data.get("password"), str) else (
                data.get("pass") if isinstance(data.get("pass"), str) else "")
            first = data.get("first").strip() if isinstance(data.get("first"), str) else ""
            last = data.get("last").strip() if isinstance(data.get("last"), str) else ""
            bad = {"detail": "رمز عبور یا اثر انگشت نادرست است."}
            st = get_state()
            users = st.get("users") or {}
            uk = uk.strip()
            u = users.get(uk) if uk else None
            if not isinstance(u, dict) and first and last:
                for k, uu in users.items():
                    if uu and uu.get("first") == first and uu.get("last") == last:
                        uk, u = k, uu
                        break
            known = isinstance(u, dict)
            akey = uk if known else (decoy_key(first, last) if (first and last) else "x" + hashlib.sha256(uk.encode("utf-8", "replace")).hexdigest()[:12])
            wait = max(lock_remaining("lip:" + ip), lock_remaining("lacct:" + akey))
            if wait:
                return self._locked(wait)
            if known and ADMIN_FP_ONLY and u.get("role") == "admin" and user_creds(uk):
                log_event("admin_password_refused", uk, ip)
                return self._json(400, {"detail": "برای حساب مدیر فقط ورود با اثر انگشت مجاز است."})
            if needs_challenge(akey, ip):
                verdict = check_captcha(data.get("captcha_id"), data.get("captcha_answer"))
                if verdict != "ok":
                    rate_fail("lip:" + ip)
                    log_event("captcha_fail", uk if known else None, ip, {"why": verdict})
                    msg = ("پاسخ را خیلی سریع دادی؛ چند ثانیه صبر کن و دوباره امتحان کن." if verdict == "early"
                           else "پاسخ چالش امنیتی نادرست است.")
                    return self._json(400, {"detail": msg, "challenge": challenge_for(akey, ip)})
            wait = max(attempt_gate("lip:" + ip, 40), attempt_gate("lacct:" + akey, RATE_MAX))
            if wait:
                return self._locked(wait)
            if not known:
                burn_dummy_verify(raw_pw[:PW_MAX])
                ok, upgrade = False, False
            elif not raw_pw or len(raw_pw) > PW_MAX or "\x00" in raw_pw:
                ok, upgrade = False, False
            else:
                ok, upgrade = check_pw(u, raw_pw)
            if not ok:
                log_event("login_fail" if known else "login_unknown", uk if known else None, ip)
                with _lock:
                    cc = db_conn()
                    nfail = cc.execute("SELECT COUNT(*) AS n FROM rate_events WHERE key=? AND ts>?",
                                       ("lip:" + ip, time.time() - RATE_WINDOW)).fetchone()["n"]
                    cc.close()
                if nfail >= 20:
                    log_event("login_burst", None, ip, {"failures": nfail})
                wait = max(rate_blocked("lip:" + ip, 40), rate_blocked("lacct:" + akey))
                if wait:
                    return self._locked(wait)
                body = dict(bad)
                ch = challenge_for(akey, ip)
                if ch:
                    body["challenge"] = ch
                return self._json(400, body)
            rate_release("lip:" + ip)
            if upgrade:
                try:
                    new_hash = hash_pw(raw_pw)
                    with _lock:
                        st = get_state()
                        cur = (st.get("users") or {}).get(uk)
                        if isinstance(cur, dict):
                            cur["pw"] = new_hash
                            cur.pop("salt", None)
                            cur.pop("password", None)
                            set_state(st)
                except RuntimeError:
                    pass
            rate_ok("lacct:" + akey)
            log_event("login_ok", uk, ip)
            return self._login_reply(uk, device, st)


        if path == "/api/backup/options":
            uk = session_user(token)
            if not uk or not self._is_admin(uk):
                return self._json(403, {"detail": "فقط مدیر."})
            creds = user_creds(uk)
            if creds:
                cid, ch = new_challenge("backup", uk)
                rp = expected_rp_id(self)
                return self._json(200, {
                    "mode": "webauthn",
                    "cid": cid,
                    "challenge": b64u_enc(ch),
                    "rpId": rp,
                    "allowCredentials": [{"type": "public-key", "id": c["cred_id"]} for c in creds],
                    "userVerification": "required",
                    "timeout": 120000,
                })
            return self._json(200, {"mode": "password", "csrf": csrf_for(token)})

        if path == "/api/backup/list":
            uk = session_user(token)
            if not uk or not self._is_admin(uk):
                return self._json(403, {"detail": "فقط مدیر."})
            return self._json(200, {"items": list_backups(), "hours": AUTO_BACKUP_HOURS, "keep": BACKUP_KEEP})

        if path in ("/api/backup/download", "/api/backup/restore"):
            uk = session_user(token)
            if not uk or not self._is_admin(uk):
                log_event("backup_denied", uk, ip, {"why": "not_admin"})
                return self._json(403, {"detail": "فقط مدیر."})
            mode = self._backup_auth(uk, data, ip)
            if not mode:
                return
            try:
                bid = int(data.get("bid") or 0)
            except (TypeError, ValueError):
                bid = 0
            if path == "/api/backup/download":
                try:
                    if bid:
                        dump_bytes = gzip.decompress(get_backup_blob(bid))
                    else:
                        dump_bytes = make_sql_backup().encode("utf-8")
                except BackupError as e:
                    return self._json(404, {"detail": str(e)})
                except Exception as e:
                    log_event("backup_error", uk, ip, {"err": type(e).__name__})
                    return self._json(500, {"detail": "خطا در ساخت بکاپ."})
                filename = "arka-backup-%s.sql" % time.strftime("%Y%m%d-%H%M%S")
                log_event("backup_ok", uk, ip, {"mode": mode, "bytes": len(dump_bytes)})
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", "attachment; filename=\"%s\"" % filename)
                self.send_header("Content-Length", str(len(dump_bytes)))
                self.send_header("Cache-Control", "no-store")
                self._sec_headers()
                self.end_headers()
                self.wfile.write(dump_bytes)
                return
            try:
                if bid:
                    raw = gzip.decompress(get_backup_blob(bid))
                else:
                    raw = base64.b64decode(data.get("file") or "")
                if len(raw) < 20:
                    raise BackupError("فایل خالی است.")
                info = restore_from_tables(parse_backup_bytes(raw), uk)
            except BackupError as e:
                return self._json(400, {"detail": str(e)})
            except Exception as e:
                log_event("backup_restore_fail", uk, ip, {"err": type(e).__name__})
                return self._json(400, {"detail": "فایل بکاپ خوانده نشد یا معتبر نیست."})
            log_event("backup_restore", uk, ip, info)
            return self._json(200, dict(info, ok=True))

        if path == "/api/session":
            if throttled("se:" + ip, 120):
                return self._locked(60)
            uk = session_user(token) or device_user(device)
            st = get_state()
            u = (st.get("users") or {}).get(uk) if uk else None
            if isinstance(u, dict):
                pu = public_user(u, uk)
                return self._json(200, {
                    "token": None,
                    "user": {"first": pu.get("first"), "last": pu.get("last"), "email": uk,
                             "fp": pu["fp"], "fp_on": pu["fp_on"]},
                    "user_key": uk,
                    "db": anonymous_state(),
                    "needs_fp": pu["fp_on"],
                    "fp_on": pu["fp_on"],
                    "lock": lock_remaining("lacct:" + uk),
                    "challenge": challenge_for(uk, ip),
                })
            return self._json(200, {"token": None, "user": None, "user_key": None, "db": anonymous_state(),
                                    "needs_fp": False, "fp_on": False})

        return self._json(404, {"detail": "not found"})


def _ver_tuple(v):
    parts = []
    for x in str(v).split("."):
        m = re.match(r"\d+", x)
        if not m:
            break
        parts.append(int(m.group(0)))
    return tuple(parts)


def dep_versions():
    from importlib import metadata
    out = {}
    for name in MIN_VERSIONS:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = None
    return out


def deps_problem():
    if TESTING:
        return None
    bad = []
    for name, ver in dep_versions().items():
        if ver is None:
            bad.append("کتابخانهٔ %s نصب نیست." % name)
        elif _ver_tuple(ver) < MIN_VERSIONS[name]:
            bad.append("%s نسخهٔ %s قدیمی است؛ حداقل %s لازم است (pip install -U -r requirements.txt)." % (
                name, ver, ".".join(map(str, MIN_VERSIONS[name]))))
    return " ".join(bad) or None


def create_admin_cli():
    st = get_state()
    if any(isinstance(u, dict) and u.get("role") == "admin" for u in (st.get("users") or {}).values()):
        print("یک مدیر از قبل وجود دارد؛ ساخت مدیر دوم از این مسیر ممکن نیست.")
        return 1
    pw = os.environ.get("ARKA_ADMIN_PASSWORD", "")
    if not pw:
        if sys.stdin.isatty():
            import getpass
            pw = getpass.getpass("رمز مدیر را وارد کن: ")
            if getpass.getpass("دوباره: ") != pw:
                print("دو رمز یکسان نیست.")
                return 1
        else:
            pw = sys.stdin.readline().rstrip("\n")
    problem = password_problem(pw, "Arka", "Member")
    if problem:
        print(problem)
        return 1
    pw_hash = hash_pw(pw)
    with _lock:
        st = get_state()
        key = "u" + uuid.uuid4().hex[:12]
        st.setdefault("users", {})[key] = {
            "first": "Arka", "last": "Member", "email": key, "avatar": "",
            "uid": str(int(1e7 + (uuid.uuid4().int % 90000000))), "joined": int(time.time() * 1000),
            "pw": pw_hash, "role": "admin"}
        st.setdefault("data", {})[key] = {"bal": 0, "tx": [], "notif": []}
        set_state(st)
    log_event("first_admin_created", key, "cli", {"how": "cli"})
    print("حساب مدیر ساخته شد. با نام «Arka» و «Member» وارد شو و بلافاصله اثر انگشت را فعال کن.")
    return 0


def remove_admin_fp_cli():
    st = get_state()
    keys = [k for k, u in (st.get("users") or {}).items() if isinstance(u, dict) and u.get("role") == "admin"]
    if not keys:
        print("مدیری پیدا نشد.")
        return 1
    with _lock:
        c = db_conn()
        for k in keys:
            c.execute("DELETE FROM webauthn_creds WHERE user_key=?", (k,))
            c.execute("DELETE FROM sessions WHERE user_key=?", (k,))
        c.commit()
        c.close()
    for k in keys:
        log_event("admin_fp_removed", k, "cli")
    print("اثر انگشت مدیر پاک شد و نشست‌هایش بسته شد. با رمز وارد شو و دوباره اثر انگشت را ثبت کن.")
    return 0



def create_db_backup_file():
    """بکاپ تک‌فایلی PostgreSQL (custom format فشرده). فقط برای ادمین احراز‌شده."""
    url = os.environ.get("DATABASE_URL") or os.environ.get("ARKA_DATABASE_URL") or ""
    if not url:
        raise RuntimeError("DATABASE_URL missing")
    # جلوگیری از injection در آرگومان‌ها — url کامل به pg_dump داده می‌شود
    fd, tmp = tempfile.mkstemp(suffix=".dump")
    os.close(fd)
    try:
        env = os.environ.copy()
        # pg_dump از URI پشتیبانی می‌کند
        cmd = ["pg_dump", "--format=custom", "--no-owner", "--file", tmp, url]
        p = subprocess.run(cmd, capture_output=True, timeout=120, env=env)
        if p.returncode != 0:
            err = (p.stderr or b"").decode("utf-8", "replace")[:300]
            raise RuntimeError("pg_dump failed: %s" % err)
        data = Path(tmp).read_bytes()
        if len(data) < 32:
            raise RuntimeError("empty dump")
        stamp = time.strftime("%Y%m%d-%H%M%S")
        return data, "arka-backup-%s.dump" % stamp
    finally:
        try:
            os.unlink(tmp)
        except Exception:
            pass


class BackupError(Exception):
    pass


def _sql_lit(v):
    if v is None:
        return "NULL"
    if isinstance(v, (bytes, bytearray, memoryview)):
        return "'\\x%s'" % bytes(v).hex()
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'" + str(v).replace("'", "''") + "'"


def build_sql_backup(meta_rows, cred_rows):
    out = ["-- Arka backup (arka-sql-1) %s" % time.strftime("%Y-%m-%d %H:%M:%S"),
           "-- PostgreSQL plain SQL; restorable with psql or from inside the admin panel",
           "SET standard_conforming_strings = on;"]
    out += [x + ";" for x in SCHEMA]
    for r in meta_rows:
        if r["key"] == "csrf_secret":
            continue
        out.append("INSERT INTO meta (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;"
                   % (_sql_lit(r["key"]), _sql_lit(r["value"])))
    for r in cred_rows:
        out.append("INSERT INTO webauthn_creds (cred_id, user_key, alg, pub, sign_count, created) VALUES (%s, %s, %s, %s, %s, %s) "
                   "ON CONFLICT (cred_id) DO UPDATE SET user_key = EXCLUDED.user_key, alg = EXCLUDED.alg, pub = EXCLUDED.pub, "
                   "sign_count = EXCLUDED.sign_count, created = EXCLUDED.created;"
                   % tuple(_sql_lit(r[k]) for k in ("cred_id", "user_key", "alg", "pub", "sign_count", "created")))
    return "\n".join(out) + "\n"


def make_sql_backup():
    with _lock:
        c = db_conn()
        try:
            meta = c.execute("SELECT key, value FROM meta").fetchall()
            creds = c.execute("SELECT cred_id, user_key, alg, pub, sign_count, created FROM webauthn_creds").fetchall()
        finally:
            c.close()
    return build_sql_backup(meta, creds)


def _ensure_backup_table(c):
    c.execute("CREATE TABLE IF NOT EXISTS backups (id BIGSERIAL PRIMARY KEY, ts DOUBLE PRECISION NOT NULL, "
              "label TEXT, size INTEGER NOT NULL, data BYTEA NOT NULL)")


def snapshot_now(label="auto"):
    gz = gzip.compress(make_sql_backup().encode("utf-8"), 6)
    with _lock:
        c = db_conn()
        try:
            _ensure_backup_table(c)
            c.execute("INSERT INTO backups(ts,label,size,data) VALUES(?,?,?,?)", (time.time(), label, len(gz), gz))
            c.execute("DELETE FROM backups WHERE id NOT IN (SELECT id FROM backups ORDER BY id DESC LIMIT ?)",
                      (max(3, BACKUP_KEEP),))
            c.commit()
        finally:
            c.close()
    return gz


def list_backups():
    with _lock:
        c = db_conn()
        try:
            _ensure_backup_table(c)
            c.commit()
            rows = c.execute("SELECT id, ts, label, size FROM backups ORDER BY id DESC LIMIT 50").fetchall()
        finally:
            c.close()
    return [{"id": r["id"], "ts": r["ts"], "label": r["label"], "size": r["size"]} for r in rows]


def get_backup_blob(bid):
    with _lock:
        c = db_conn()
        try:
            _ensure_backup_table(c)
            c.commit()
            row = c.execute("SELECT data FROM backups WHERE id=?", (bid,)).fetchone()
        finally:
            c.close()
    if not row:
        raise BackupError("این نسخهٔ بکاپ پیدا نشد.")
    return bytes(row["data"])


def _last_snapshot_ts():
    try:
        with _lock:
            c = db_conn()
            try:
                _ensure_backup_table(c)
                c.commit()
                row = c.execute("SELECT MAX(ts) AS t FROM backups").fetchone()
            finally:
                c.close()
        return (row or {}).get("t") or 0
    except Exception:
        return 0


def _send_backup_bale(name, data):
    boundary = uuid.uuid4().hex

    def field(n, v):
        return ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, n, v)).encode("utf-8")
    body = (field("chat_id", ALERT_BALE_CHAT) + field("caption", "Arka backup") +
            ('--%s\r\nContent-Disposition: form-data; name="document"; filename="%s"\r\n'
             'Content-Type: application/gzip\r\n\r\n' % (boundary, name)).encode("utf-8") +
            data + ("\r\n--%s--\r\n" % boundary).encode("utf-8"))
    req = urllib.request.Request("https://tapi.bale.ai/bot%s/sendDocument" % ALERT_BALE_TOKEN, data=body,
                                 headers={"Content-Type": "multipart/form-data; boundary=" + boundary}, method="POST")
    urllib.request.urlopen(req, timeout=90).read()


def auto_backup_tick(force=False):
    if AUTO_BACKUP_HOURS <= 0 and not force:
        return False
    if not force and time.time() - _last_snapshot_ts() < AUTO_BACKUP_HOURS * 3600:
        return False
    gz = snapshot_now("auto")
    name = "arka-auto-%s.sql.gz" % time.strftime("%Y%m%d-%H%M%S")
    if BACKUP_DIR:
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            Path(BACKUP_DIR, name).write_bytes(gz)
            old = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("arka-auto-")])
            for f in old[:-max(3, BACKUP_KEEP)]:
                os.unlink(os.path.join(BACKUP_DIR, f))
        except Exception:
            pass
    if BACKUP_SEND_BALE and ALERT_BALE_TOKEN and ALERT_BALE_CHAT:
        threading.Thread(target=lambda: _try(lambda: _send_backup_bale(name, gz)), daemon=True).start()
    return True


def _try(fn):
    try:
        fn()
    except Exception:
        pass


# ----- reading backups: plain SQL, pg_dump plain, pg_dump custom (.dump), gzip of those -----
_WANT = ("meta", "webauthn_creds")
_COPY_ESC = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v"}


def _copy_unescape(v):
    if v == "\\N":
        return None
    if "\\" not in v:
        return v
    out, i = [], 0
    while i < len(v):
        ch = v[i]
        if ch == "\\" and i + 1 < len(v):
            out.append(_COPY_ESC.get(v[i + 1], v[i + 1]))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _copy_header(line):
    m = re.match(r'^COPY\s+(?:"?\w+"?\.)?"?(\w+)"?\s*\(([^)]*)\)\s+FROM\s+stdin;?', line.strip(), re.I)
    if not m:
        return None
    return m.group(1), [c.strip().strip('"') for c in m.group(2).split(",")]


def _copy_rows(cols, text):
    rows = []
    for ln in text.split("\n"):
        if ln == "\\.":
            break
        if ln == "":
            continue
        vals = [_copy_unescape(x) for x in ln.split("\t")]
        if len(vals) == len(cols):
            rows.append(dict(zip(cols, vals)))
    return rows


_STR_RE = re.compile(r"'[^']*(?:''[^']*)*'")
_TOK_RE = re.compile(r"'[^']*(?:''[^']*)*'|--[^\n]*|;")
_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_INS_RE = re.compile(r'^INSERT\s+INTO\s+(?:"?\w+"?\.)?"?(\w+)"?\s*\(([^)]*)\)\s*VALUES\s*\(', re.I)


def _parse_values(t, i):
    vals, n = [], len(t)
    while i < n:
        while i < n and t[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        if t[i] == "'":
            m = _STR_RE.match(t, i)
            if not m:
                raise BackupError("فایل SQL خراب است.")
            vals.append(m.group(0)[1:-1].replace("''", "'"))
            i = m.end()
        elif t[i:i + 4].upper() == "NULL":
            vals.append(None)
            i += 4
        elif t[i:i + 4].upper() == "TRUE":
            vals.append(True)
            i += 4
        elif t[i:i + 5].upper() == "FALSE":
            vals.append(False)
            i += 5
        else:
            m = _NUM_RE.match(t, i)
            if not m:
                raise BackupError("مقدار نامعتبر در فایل SQL.")
            x = m.group(0)
            vals.append(float(x) if re.search(r"[.eE]", x) else int(x))
            i = m.end()
        while i < n and t[i] in " \t\r\n":
            i += 1
        if i < n and t[i] == ",":
            i += 1
            continue
        break
    return vals


def _parse_sql_text(text):
    tables = {}
    rest, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("COPY ") and ln.rstrip().endswith("FROM stdin;"):
            hdr = _copy_header(ln)
            j = i + 1
            while j < len(lines) and lines[j] != "\\.":
                j += 1
            if hdr and hdr[0] in _WANT:
                tables.setdefault(hdr[0], []).extend(_copy_rows(hdr[1], "\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        rest.append(ln)
        i += 1
    t = "\n".join(rest)
    parts, start = [], 0
    for m in _TOK_RE.finditer(t):
        g = m.group(0)
        if g.startswith("--"):
            parts.append(t[start:m.start()])
            start = m.end()
        elif g == ";":
            parts.append(t[start:m.start()])
            stmt = "".join(parts).strip()
            parts, start = [], m.end()
            mm = _INS_RE.match(stmt)
            if mm and mm.group(1) in _WANT:
                cols = [c.strip().strip('"') for c in mm.group(2).split(",")]
                vals = _parse_values(stmt, mm.end())
                if len(vals) == len(cols):
                    tables.setdefault(mm.group(1), []).append(dict(zip(cols, vals)))
    return tables


class _Rd:
    def __init__(self, b, isz=4):
        self.b, self.i, self.isz = b, 0, isz

    def byte(self):
        if self.i >= len(self.b):
            raise BackupError("فایل بکاپ ناقص است.")
        v = self.b[self.i]
        self.i += 1
        return v

    def raw(self, n):
        if n < 0 or self.i + n > len(self.b):
            raise BackupError("فایل بکاپ ناقص است.")
        v = self.b[self.i:self.i + n]
        self.i += n
        return v

    def int(self):
        sign = self.byte()
        n = int.from_bytes(self.raw(self.isz), "little")
        return -n if sign else n

    def str(self):
        n = self.int()
        return None if n < 0 else self.raw(n).decode("utf-8", "replace")


def _parse_pgdump_custom(b):
    r = _Rd(b)
    r.raw(5)
    vmaj, vmin = r.byte(), r.byte()
    vrev = r.byte() if (vmaj > 1 or vmin > 0) else 0
    ver = (vmaj, vmin, vrev)
    r.isz = r.byte()
    offsz = r.byte() if ver >= (1, 7, 0) else r.isz
    if r.byte() != 1:
        raise BackupError("فقط بکاپ‌های pg_dump با فرمت custom یا SQL متنی پشتیبانی می‌شود.")
    if ver >= (1, 15, 0):
        alg = r.byte()
    else:
        alg = 0 if r.int() == 0 else 1
    if alg not in (0, 1):
        raise BackupError("بکاپ با فشرده‌سازی lz4/zstd گرفته شده؛ آن را با فرمت SQL متنی یا gzip دوباره بگیر.")
    for _ in range(7):
        r.int()
    r.str()
    if ver >= (1, 10, 0):
        r.str()
        r.str()
    cnt = r.int()
    toc = []
    for _ in range(cnt):
        did = r.int()
        r.int()
        r.str()
        r.str()
        tag = r.str()
        desc = r.str()
        r.int()
        r.str()
        r.str()
        copy = r.str()
        r.str()
        r.str()
        if ver >= (1, 14, 0):
            r.str()
        if ver >= (1, 16, 0):
            r.int()
        r.str()
        r.str()
        while r.str() is not None:
            pass
        r.byte()
        r.raw(offsz)
        toc.append((did, tag, desc, copy))
    blocks = {}
    while r.i < len(b):
        bt = r.byte()
        if bt == 1:
            did = r.int()
            chunks = []
            while True:
                n = r.int()
                if n == 0:
                    break
                chunks.append(r.raw(n))
            data = b"".join(chunks)
            blocks[did] = zlib.decompress(data) if alg == 1 and data else data
        elif bt == 3:
            while r.int() != 0:
                n = r.int()
                while n != 0:
                    r.raw(n)
                    n = r.int()
        else:
            break
    tables = {}
    for did, tag, desc, copy in toc:
        if desc != "TABLE DATA" or tag not in _WANT or did not in blocks:
            continue
        hdr = _copy_header(copy or "")
        if hdr:
            tables.setdefault(hdr[0], []).extend(_copy_rows(hdr[1], blocks[did].decode("utf-8", "replace")))
    return tables


def parse_backup_bytes(raw):
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    if raw[:5] == b"PGDMP":
        tables = _parse_pgdump_custom(raw)
    else:
        tables = _parse_sql_text(raw.decode("utf-8", "replace"))
    for r in tables.get("webauthn_creds") or []:
        p = r.get("pub")
        if isinstance(p, str):
            r["pub"] = bytes.fromhex(p[2:] if p.startswith("\\x") else p)
    return tables


def restore_from_tables(tables, who):
    st_raw = None
    for r in tables.get("meta") or []:
        if r.get("key") == "state":
            st_raw = r.get("value")
    if not st_raw:
        raise BackupError("داخل این فایل اطلاعات آرکا (جدول meta/state) پیدا نشد.")
    try:
        st = json.loads(st_raw)
    except Exception:
        raise BackupError("اطلاعات داخل فایل خراب است.")
    if state_problem(st):
        raise BackupError("ساختار اطلاعات داخل فایل معتبر نیست.")
    users = st.get("users") or {}
    if not any(isinstance(u, dict) and u.get("role") == "admin" for u in users.values()):
        raise BackupError("در این بکاپ هیچ ادمینی نیست؛ بازیابی انجام نشد.")
    creds = tables.get("webauthn_creds")
    with _lock:
        cur = get_state()
        if cur.get("users"):
            snapshot_now("pre-restore")
        for k in ("oid", "tid", "payc"):
            st[k] = int(max(_num(st.get(k)), _num(cur.get(k))))
        st["rev"] = int(max(_num(st.get("rev")), _num(cur.get("rev")))) + 1
        st.pop("snap", None)
        st.pop("_fl", None)
        set_state(st)
        if creds is not None:
            c = db_conn()
            try:
                c.execute("DELETE FROM webauthn_creds")
                for r in creds:
                    c.execute("INSERT INTO webauthn_creds(cred_id,user_key,alg,pub,sign_count,created) VALUES(?,?,?,?,?,?) "
                              "ON CONFLICT (cred_id) DO NOTHING",
                              (r["cred_id"], r["user_key"], int(r["alg"]), r["pub"], int(r.get("sign_count") or 0),
                               float(r.get("created") or time.time())))
                c.commit()
            finally:
                c.close()
        removed = [k for k in (cur.get("users") or {}) if k not in users]
    drop_user_auth(removed)
    return {"users": len(users), "orders": len(st.get("orders") or []), "pays": len(st.get("pays") or []),
            "tickets": len(st.get("tickets") or [])}


def maybe_auto_restore():
    """اگر دیتابیس خالی است (مثلاً Railway دیتابیس را از صفر ساخته)، از فایل بکاپ بازیابی می‌کند."""
    try:
        if (get_state().get("users") or {}):
            return
        path = RESTORE_FILE
        if not path and BACKUP_DIR and os.path.isdir(BACKUP_DIR):
            fs = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith("arka-") and ".sql" in f]
            path = max(fs, key=os.path.getmtime) if fs else ""
        if path and os.path.isfile(path):
            info = restore_from_tables(parse_backup_bytes(Path(path).read_bytes()), None)
            print("بازیابی خودکار از %s انجام شد: %s" % (path, info))
    except Exception as e:
        print("بازیابی خودکار ناموفق بود: %s" % (e,))


def backup_status():
    last = _last_snapshot_ts()
    if BACKUP_DIR:
        try:
            files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith("arka-") and ".sql" in f]
        except OSError:
            files = []
        if files:
            last = max(last, max(os.path.getmtime(f) for f in files))
    if not last:
        return False, "هنوز هیچ بکاپی گرفته نشده"
    age_h = (time.time() - last) / 3600.0
    if age_h > BACKUP_MAX_HOURS:
        return False, "آخرین پشتیبان %d ساعت پیش بوده (حداکثر مجاز %d)" % (age_h, BACKUP_MAX_HOURS)
    return True, "آخرین پشتیبان %d ساعت پیش" % age_h



def housekeeping():
    now = time.time()
    with _lock:
        c = db_conn()
        c.execute("DELETE FROM sessions WHERE created<?", (now - SESSION_TTL,))
        c.execute("DELETE FROM locks WHERE until_ts<?", (now,))
        c.execute("DELETE FROM lock_levels WHERE ts<?", (now - LEVEL_DECAY,))
        c.execute("DELETE FROM challenges WHERE exp<?", (now,))
        c.execute("DELETE FROM rate_events WHERE ts<?", (now - RATE_WINDOW,))
        c.execute("DELETE FROM security_log WHERE ts<?", (now - LOG_RETENTION,))
        c.commit()
        c.close()
    try:
        auto_backup_tick()
    except Exception as e:
        sys.stderr.write("auto backup failed: %s\n" % type(e).__name__)
    ok, msg = backup_status()
    if ok is False:
        log_event("backup_stale", None, None, {"why": msg})
    return ok, msg


def _watchdog(interval=3600):
    while True:
        time.sleep(interval)
        try:
            housekeeping()
        except Exception:
            pass


class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 128

    def __init__(self, *a, **k):
        self._slots = threading.BoundedSemaphore(MAX_CONNECTIONS)
        super().__init__(*a, **k)

    def process_request(self, request, client_address):
        if not self._slots.acquire(blocking=False):
            try:
                request.sendall(b"HTTP/1.0 503 Service Unavailable\r\nContent-Length: 0\r\n\r\n")
            except Exception:
                pass
            self.shutdown_request(request)
            return
        super().process_request(request, client_address)

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._slots.release()


def _mask_dsn(url):
    try:
        p = urlparse(url)
        return "%s:%s/%s" % (p.hostname or "?", p.port or 5432, (p.path or "").lstrip("/"))
    except Exception:
        return "?"


def main():
    if psycopg is None:
        print("درایور PostgreSQL نصب نیست. این دستور را اجرا کن:")
        print('    pip install "psycopg[binary]"')
        return
    if not ARGON2 and not ALLOW_PBKDF2_FALLBACK:
        print("کتابخانهٔ argon2-cffi نصب نیست. برای هش امن رمزها این دستور را اجرا کن:")
        print("    pip install argon2-cffi")
        return
    problem = secret_file_problem()
    if problem:
        print(problem)
        return
    url = database_url()
    if not url:
        print("آدرس دیتابیس تنظیم نشده. مثال:")
        print("    export DATABASE_URL='postgresql://arka:RAMZ@localhost:5432/arka'")
        return
    cert, key = os.environ.get("ARKA_TLS_CERT"), os.environ.get("ARKA_TLS_KEY")
    if PRODUCTION:
        bad = []
        if TESTING:
            bad.append("ARKA_TESTING نباید در production روشن باشد.")
        if HOST in ("0.0.0.0", "::", ""):
            bad.append("در production آدرس گوش‌دادن نباید 0.0.0.0 باشد؛ ARKA_HOST=127.0.0.1 (پشت nginx) یا IP مشخص سرور را بده.")
        if CHALLENGE_DELAY_BASE < 2:
            bad.append("ARKA_CHALLENGE_DELAY در production حداقل ۲ ثانیه باشد.")
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            bad.append("برنامه را با کاربر root اجرا نکن؛ یک کاربر معمولی (مثلاً arka) بساز.")
        dp = deps_problem()
        if dp:
            bad.append(dp)
        if LOCK_SECONDS < 60:
            bad.append("ARKA_LOCK_SECONDS در production حداقل ۶۰ باشد.")
        if SOCKET_TIMEOUT > 120 or SOCKET_TIMEOUT < 1:
            bad.append("ARKA_SOCKET_TIMEOUT باید بین ۱ تا ۱۲۰ ثانیه باشد.")
        if TRUST_PROXY and not (cert and key) and HOST not in ("127.0.0.1", "::1", "localhost"):
            bad.append("با ARKA_TRUST_PROXY=1 برنامه باید فقط روی 127.0.0.1 گوش بدهد (ARKA_HOST=127.0.0.1).")
        if not ALLOWED_HOSTS:
            bad.append("در حالت production باید دامنه‌های مجاز را بدهی: ARKA_ALLOWED_HOSTS=example.com")
        if not (cert and key) and not TRUST_PROXY:
            bad.append("حالت production بدون HTTPS اجرا نمی‌شود: ARKA_TLS_CERT و ARKA_TLS_KEY را بده، "
                       "یا پشت پروکسی HTTPS (مثل nginx) با ARKA_TRUST_PROXY=1 اجرا کن.")
        host = (urlparse(url).hostname or "").lower()
        if host not in ("localhost", "127.0.0.1", "::1", "") and "sslmode=require" not in url \
                and "sslmode=verify" not in url:
            bad.append("اتصال به دیتابیس غیرمحلی باید رمزنگاری‌شده باشد: به آدرس دیتابیس ?sslmode=require اضافه کن.")
        if bad:
            for m in bad:
                print(m)
            return
    try:
        init_db()
    except Exception as e:
        print("اتصال به PostgreSQL یا ساخت جدول‌ها ناموفق بود (%s). آدرس، کاربر و رمز دیتابیس را بررسی کن." % type(e).__name__)
        return
    if "--audit" in sys.argv:
        for k, v in audit_passwords().items():
            print("%-14s %d" % (k, v))
        for k, v in dep_versions().items():
            print("%-14s %s (حداقل %s)" % (k, v or "نصب نیست", ".".join(map(str, MIN_VERSIONS[k]))))
        print("به‌روزرسانی/ممیزی: pip-audit -r requirements.txt")
        return
    if "--create-admin" in sys.argv:
        create_admin_cli()
        return
    if "--remove-admin-fp" in sys.argv:
        remove_admin_fp_cli()
        return
    if "--backup-status" in sys.argv:
        ok, msg = backup_status()
        print(("OK: " if ok else ("هشدار: " if ok is False else "")) + msg)
        return
    if "--init-db" in sys.argv:
        print("جدول‌ها و داده‌ها آماده است.")
        return
    if "--revoke-all-sessions" in sys.argv:
        with _lock:
            c = db_conn()
            c.execute("DELETE FROM sessions")
            c.commit()
            c.close()
        print("همهٔ نشست‌ها باطل شد؛ همه باید دوباره وارد شوند.")
        return
    if "--rotate-csrf-secret" in sys.argv:
        with _lock:
            c = db_conn()
            c.execute("UPDATE meta SET value=? WHERE key='csrf_secret'", (secrets.token_hex(32),))
            c.commit()
            c.close()
        print("کلید CSRF عوض شد؛ صفحه‌ها باید یک‌بار تازه‌سازی شوند.")
        return
    if "--security-log" in sys.argv:
        try:
            n = int(sys.argv[sys.argv.index("--security-log") + 1])
        except (ValueError, IndexError):
            n = 50
        c = db_conn()
        for r in c.execute("SELECT ts,event,user_key,ip,detail FROM security_log ORDER BY id DESC LIMIT ?",
                           (max(1, min(n, 1000)),)).fetchall():
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r["ts"])), r["event"], r["user_key"] or "-",
                  r["ip"] or "-", r["detail"] or "")
        c.close()
        return
    if PRODUCTION and not (ALERT_WEBHOOK or (ALERT_BALE_TOKEN and ALERT_BALE_CHAT)):
        print("هشدار: هیچ کانال هشدار فوری تنظیم نشده (ARKA_ALERT_WEBHOOK یا ARKA_ALERT_BALE_TOKEN + ARKA_ALERT_BALE_CHAT).")
    if PRODUCTION and not BACKUP_DIR:
        print("هشدار: ARKA_BACKUP_DIR تنظیم نشده؛ تازه بودن پشتیبان کنترل نمی‌شود.")
    maybe_auto_restore()
    if "--restore" in sys.argv:
        try:
            f = sys.argv[sys.argv.index("--restore") + 1]
            print("بازیابی انجام شد:", restore_from_tables(parse_backup_bytes(Path(f).read_bytes()), None))
        except Exception as e:
            print("بازیابی ناموفق:", e)
        return
    threading.Thread(target=lambda: _try(housekeeping), daemon=True).start()
    threading.Thread(target=_watchdog, daemon=True).start()
    if get_state().get("products") is None:
        print("هشدار: کاتالوگ محصولات هنوز روی سرور ذخیره نشده. مدیر یک‌بار وارد بخش محصولات شود تا اعتبارسنجی قیمت سفارش‌ها فعال شود.")
    try:
        httpd = Server((HOST, PORT), Handler)
        if cert and key:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            ctx.load_cert_chain(cert, key)
            httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    except OSError as e:
        print("خطا در باز کردن پورت %s: %s" % (PORT, e))
        print("اگر پورت اشغال است، برنامهٔ قبلی را ببند و دوباره Run کن.")
        return
    print("=" * 44)
    print("  Arka آماده است")
    print("  %s://localhost:%s" % ("https" if cert else "http", PORT))
    print("  دیتابیس: PostgreSQL %s" % _mask_dsn(url))
    print("  حالت: %s" % ("production" if PRODUCTION else "توسعه"))
    if HOST in ("0.0.0.0", "::"):
        print("  هشدار: سرور روی همهٔ شبکه باز است. فقط پشت دیوارآتش/پروکسی HTTPS استفاده کن.")
    print("  اثر انگشت فقط روی localhost یا HTTPS با دامنه کار می‌کند")
    print("=" * 44)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتوقف")
        httpd.server_close()


if __name__ == "__main__":
    main()
