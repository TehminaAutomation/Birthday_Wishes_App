import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Happy Birthday My Jaan ❤️",
    page_icon="🎂",
    layout="wide",
)

st.markdown(
    """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        background: #08030d;
    }

    iframe {
        border: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# PATHS
# ============================================================

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")


# ============================================================
# ASSET LOADER
# ============================================================

def asset(name, audio=False):
    path = os.path.join(ASSETS, name)

    if not os.path.exists(path):
        return ""

    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")

        if audio:
            return "data:audio/mpeg;base64," + data

        ext = os.path.splitext(name)[1].lower()

        mime = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }.get(ext, "image/jpeg")

        return f"data:{mime};base64,{data}"

    except Exception:
        return ""


# ============================================================
# LOAD ASSETS
# ============================================================

wife = asset("Wife.png")
husband = asset("Husband.jpg")
music = asset("music.mp3", audio=True)

photos = []

for i in range(1, 9):
    photo = asset(f"photo{i}.jpg")

    if photo:
        photos.append(photo)


# ============================================================
# SAFE JSON
# ============================================================

photos_json = json.dumps(photos)
wife_json = json.dumps(wife)
husband_json = json.dumps(husband)
music_json = json.dumps(music)


# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

html = r'''
<!doctype html>

<html>

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width,initial-scale=1"
>

<style>

/* ============================================================
GLOBAL
============================================================ */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html,
body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family:
        "Segoe UI",
        Arial,
        sans-serif;
}

#app {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(
            circle at 50% 35%,
            #8d2c68,
            #2b0d30 55%,
            #050207
        );
}


/* ============================================================
SCENES
============================================================ */

.scene {
    position: absolute;
    inset: 0;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-align: center;

    padding: 20px 15px 90px;

    opacity: 0;
    visibility: hidden;

    transform: scale(1.06);

    transition:
        opacity 0.9s ease,
        transform 0.9s ease;

    overflow: hidden;
}

.scene.active {
    opacity: 1;
    visibility: visible;
    transform: scale(1);
}

.light {
    background:
        radial-gradient(
            circle at 50% 30%,
            #fffafd,
            #ffd0e5 48%,
            #9b376f
        );
}


/* ============================================================
TEXT
============================================================ */

h1 {
    font-size: clamp(34px, 6vw, 76px);

    color: white;

    text-shadow:
        0 0 20px #ff8fc7,
        0 0 45px #ff198d;

    z-index: 10;
}

.light h1 {
    color: #97155e;

    text-shadow:
        0 5px 25px white,
        0 0 30px #ff94c8;
}

.kicker {
    color: #ffbddd;

    font-weight: 900;

    letter-spacing: 4px;

    margin-bottom: 14px;

    z-index: 10;
}

.light .kicker {
    color: #a71965;
}

.msg {
    max-width: 850px;

    margin-top: 18px;

    color: #ffe1f0;

    font-size: clamp(16px, 2.2vw, 24px);

    line-height: 1.6;

    z-index: 10;
}

.light .msg {
    color: #63264d;
}

.date {
    color: #ffb6db;

    font-size: clamp(30px, 6vw, 72px);

    font-weight: 900;

    letter-spacing: 5px;

    text-shadow:
        0 0 35px #ff2992;

    z-index: 10;
}


/* ============================================================
OPEN SCREEN
============================================================ */

#open {
    position: absolute;
    inset: 0;

    z-index: 99999;

    display: flex;

    align-items: center;
    justify-content: center;

    flex-direction: column;

    text-align: center;

    background:
        radial-gradient(
            circle at center,
            #8b2b68,
            #2b0d30 55%,
            #050207
        );

    transition: 1s;
}

.hide {
    opacity: 0 !important;
    visibility: hidden !important;
}

.openheart {
    font-size: clamp(70px, 13vw, 150px);

    animation:
        beat 1s infinite;

    filter:
        drop-shadow(0 0 25px #ff4b9d);
}

.opentitle {
    color: white;

    font-size: clamp(30px, 6vw, 70px);

    font-weight: 900;

    text-shadow:
        0 0 25px #ff62b1;

    margin: 10px;
}

.openmsg {
    color: #ffd8ed;

    font-size: 20px;

    margin: 10px 20px 25px;
}

.openbtn,
.musicbtn {
    border: 0;

    border-radius: 30px;

    padding: 12px 24px;

    background:
        linear-gradient(
            135deg,
            #ff4d9b,
            #9d185f
        );

    color: white;

    font-weight: 900;

    cursor: pointer;

    box-shadow:
        0 0 30px #ff4d9b80;

    transition: 0.3s;
}

.openbtn:hover,
.musicbtn:hover {
    transform: scale(1.06);
}

@keyframes beat {

    50% {
        transform: scale(1.14);
    }
}


/* ============================================================
PHOTO
============================================================ */

.photo {
    width: clamp(190px, 30vw, 340px);

    height: clamp(245px, 43vw, 440px);

    padding: 8px;

    margin-top: 15px;

    border-radius: 34px;

    background:
        linear-gradient(
            135deg,
            #fff,
            #ff78b9,
            #f8d978,
            #fff
        );

    box-shadow:
        0 25px 70px #30002080;

    z-index: 5;

    animation:
        float 4s infinite;
}

.photo img {
    width: 100%;
    height: 100%;

    object-fit: cover;

    border: 5px solid white;

    border-radius: 27px;
}

@keyframes float {

    50% {
        transform:
            translateY(-12px);
    }
}


/* ============================================================
COUPLE
============================================================ */

.couple {
    display: flex;

    align-items: center;

    gap: 15px;

    z-index: 5;
}

.cp {
    width: clamp(115px, 19vw, 250px);

    height: clamp(165px, 30vw, 345px);

    padding: 7px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            #fff,
            #ff93c8,
            #e9c56b
        );

    box-shadow:
        0 20px 60px #30002080;
}

.cp img {
    width: 100%;
    height: 100%;

    object-fit: cover;

    border: 4px solid white;

    border-radius: 22px;
}

.heartbig {
    font-size: clamp(40px, 6vw, 75px);

    animation:
        beat 1s infinite;
}


/* ============================================================
MEMORIES
============================================================ */

.memory {
    position: relative;

    width: clamp(210px, 34vw, 380px);

    height: clamp(270px, 48vw, 480px);

    z-index: 5;

    margin-top: 10px;
}

.memory img {
    position: absolute;

    inset: 0;

    width: 100%;
    height: 100%;

    object-fit: cover;

    border: 8px solid white;

    border-radius: 30px;

    opacity: 0;

    transform:
        scale(0.85)
        rotate(-5deg);

    transition: 0.7s;

    box-shadow:
        0 20px 70px #30002080;
}

.memory img.on {
    opacity: 1;

    transform:
        scale(1)
        rotate(0);
}

.count {
    color: #a41b68;

    font-weight: 900;

    z-index: 5;

    margin-top: 10px;
}


/* ============================================================
BALLOONS
============================================================ */

.balloonstage {
    height: 270px;

    width: 100%;

    display: flex;

    align-items: flex-end;

    justify-content: center;

    gap: clamp(3px, 1vw, 16px);

    z-index: 5;
}

.balloon {
    width: clamp(45px, 7vw, 80px);

    height: clamp(68px, 10vw, 110px);

    border-radius: 50%;

    opacity: 0;

    transform:
        translateY(280px)
        scale(0.2);

    position: relative;
}

.balloon:after {
    content: "";

    position: absolute;

    bottom: -115px;

    left: 50%;

    height: 110px;

    width: 2px;

    background: #49233e;
}

.balloon span {
    position: absolute;

    top: 45%;
    left: 50%;

    transform:
        translate(-50%, -50%);

    font-size: 9px;

    font-weight: 900;

    color: white;

    width: 90px;
}

.b1 {
    background: #ff4b91;
}

.b2 {
    background: white;

    box-shadow:
        0 0 25px white;
}

.b3 {
    background: #bd70da;
}

.b4 {
    background: #ff927d;
}

.b5 {
    background: #ec417e;
}

.b6 {
    background: #d9a1c3;
}

.rise {
    animation:
        rise 1s forwards;
}

.pop {
    animation:
        pop 0.6s forwards;
}

@keyframes rise {

    70% {
        opacity: 1;

        transform:
            translateY(-10px)
            scale(1.08);
    }

    100% {
        opacity: 1;

        transform: none;
    }
}

@keyframes pop {

    45% {
        opacity: 1;

        transform:
            scale(1.35);
    }

    100% {
        opacity: 0;

        transform:
            scale(2);
    }
}


/* ============================================================
WISH
============================================================ */

.wish {
    color: #9a165f;

    font-size: clamp(22px, 4vw, 48px);

    font-weight: 900;

    opacity: 0;

    min-height: 50px;

    z-index: 5;
}

.wish.show {
    animation:
        wish 0.7s forwards;
}

.wishdesc {
    color: #67264e;

    font-size: clamp(15px, 2vw, 21px);

    z-index: 5;
}

@keyframes wish {

    70% {
        transform:
            scale(1.08);
    }

    100% {
        opacity: 1;

        transform:
            scale(1);
    }
}


/* ============================================================
LETTER
============================================================ */

.letter {
    width: min(850px, 92vw);

    max-height: 62vh;

    overflow: auto;

    padding: 34px 38px;

    border-radius: 32px;

    background:
        linear-gradient(
            145deg,
            #fffdfef5,
            #fff1f8f5
        );

    border: 2px solid white;

    box-shadow:
        0 25px 75px #30002050,
        0 0 40px #ff6fae40;

    color: #61284e;

    font-size: clamp(15px, 2vw, 20px);

    line-height: 1.9;

    text-align: left;

    white-space: pre-line;

    z-index: 5;

    position: relative;
}

.letter:before {
    content: "❤️";

    position: absolute;

    top: 10px;
    right: 18px;

    font-size: 28px;

    animation:
        beat 1s infinite;
}


/* ============================================================
GIFTS
============================================================ */

.gifts {
    display: flex;

    gap: 20px;

    z-index: 5;

    margin: 25px 10px 15px;

    align-items: flex-end;
}

.gift {
    width: 105px;

    height: 145px;

    position: relative;

    animation:
        giftFloat 1.6s infinite alternate;

    cursor: pointer;
}

.gift:nth-child(2) {
    animation-delay: 0.2s;
}

.gift:nth-child(3) {
    animation-delay: 0.4s;
}

.gift:nth-child(4) {
    animation-delay: 0.6s;
}

@keyframes giftFloat {

    from {
        transform:
            translateY(0);
    }

    to {
        transform:
            translateY(-10px);
    }
}

.box {
    position: absolute;

    bottom: 0;
    left: 4px;

    width: 98px;
    height: 75px;

    background:
        linear-gradient(
            135deg,
            #ff62a3,
            #c91b6d
        );

    border-radius: 8px;

    box-shadow:
        0 12px 25px #9d185955;
}

.lid {
    position: absolute;

    top: 42px;
    left: -2px;

    width: 110px;
    height: 27px;

    background:
        linear-gradient(
            135deg,
            #ff75ae,
            #e03b83
        );

    border-radius: 7px;

    z-index: 2;

    transition:
        0.9s cubic-bezier(.17,.67,.3,1.4);

    transform-origin:
        15% 100%;
}

.ribbon {
    position: absolute;

    left: 45px;
    top: 42px;

    width: 18px;
    height: 103px;

    background:
        linear-gradient(
            #ffe27a,
            #ffc936
        );

    z-index: 3;
}

.ribbon:after {
    content: "";

    position: absolute;

    top: 0;
    left: -42px;

    width: 100px;
    height: 16px;

    background:
        #ffd85c;

    border-radius: 50%;
}

.gift.open .lid {
    transform:
        translateY(-70px)
        translateX(12px)
        rotate(-22deg);
}

.gift-message {
    position: absolute;

    left: 50%;

    bottom: 88px;

    width: 190px;

    transform:
        translateX(-50%)
        translateY(25px)
        scale(0.4);

    opacity: 0;

    z-index: 20;

    pointer-events: none;

    padding: 10px 14px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #fff,
            #fff0f7
        );

    border: 2px solid #ff80b8;

    color: #a71965;

    font-weight: 900;

    font-size: 14px;

    box-shadow:
        0 10px 35px #ff3d9850;
}

.gift.open .gift-message {
    animation:
        giftMessage 1.4s
        cubic-bezier(.17,.67,.3,1.2)
        forwards;
}

@keyframes giftMessage {

    0% {
        opacity: 0;

        transform:
            translateX(-50%)
            translateY(25px)
            scale(0.4);
    }

    45% {
        opacity: 1;

        transform:
            translateX(-50%)
            translateY(-25px)
            scale(1.05);
    }

    100% {
        opacity: 1;

        transform:
            translateX(-50%)
            translateY(-5px)
            scale(1);
    }
}

.gift-spark {
    position: absolute;

    left: 50%;
    top: 20px;

    transform:
        translateX(-50%)
        scale(0);

    opacity: 0;

    font-size: 25px;

    z-index: 25;
}

.gift.open .gift-spark {
    animation:
        sparkPop 1s forwards;
}

@keyframes sparkPop {

    0% {
        opacity: 0;
        transform:
            translateX(-50%)
            scale(0);
    }

    50% {
        opacity: 1;
        transform:
            translateX(-50%)
            translateY(-30px)
            scale(1.5);
    }

    100% {
        opacity: 0;
        transform:
            translateX(-50%)
            translateY(-65px)
            scale(0.7);
    }
}

.gift-center-wish {
    min-height: 65px;

    max-width: 850px;

    color: #9a165f;

    font-size:
        clamp(19px, 3vw, 32px);

    font-weight: 900;

    z-index: 10;

    opacity: 0;

    transform:
        translateY(15px)
        scale(.95);

    transition: 0.5s;
}

.gift-center-wish.show {
    opacity: 1;

    transform:
        translateY(0)
        scale(1);
}

.gift-center-desc {
    max-width: 760px;

    color: #67264e;

    font-size:
        clamp(14px, 2vw, 19px);

    min-height: 45px;

    z-index: 10;
}


/* ============================================================
ROSE GARDEN
============================================================ */

.rose-garden {
    position: relative;

    width: min(850px, 96vw);

    height: 330px;

    display: flex;

    align-items: flex-end;

    justify-content: center;

    gap: clamp(25px, 7vw, 80px);

    z-index: 5;

    margin-top: 5px;
}

.rose-item {
    position: relative;

    width: 150px;

    height: 300px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: flex-end;

    opacity: 0;

    transform:
        translateY(80px)
        scale(.7);
}

.rose-item.bloom {
    animation:
        roseBloom 1.3s
        cubic-bezier(.17,.67,.3,1.3)
        forwards;
}

.rose-item:nth-child(2) {
    animation-delay: .35s;
}

.rose-item:nth-child(3) {
    animation-delay: .7s;
}

@keyframes roseBloom {

    0% {
        opacity: 0;

        transform:
            translateY(80px)
            scale(.65);
    }

    70% {
        opacity: 1;

        transform:
            translateY(-8px)
            scale(1.08);
    }

    100% {
        opacity: 1;

        transform:
            translateY(0)
            scale(1);
    }
}

.rose-glow {
    position: absolute;

    top: 15px;

    width: 125px;
    height: 125px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #ff75b766,
            transparent 65%
        );

    filter:
        blur(8px);

    animation:
        roseGlow 2s infinite alternate;
}

@keyframes roseGlow {

    to {
        transform:
            scale(1.18);

        opacity: .7;
    }
}

.rose-flower {
    position: relative;

    width: 125px;
    height: 125px;

    z-index: 5;

    display: flex;

    align-items: center;

    justify-content: center;

    filter:
        drop-shadow(
            0 8px 18px #9b174f55
        );

    animation:
        flowerSway 3s infinite ease-in-out;
}

.rose-flower span {
    position: absolute;

    width: 58px;
    height: 58px;

    border-radius:
        50% 50%
        45% 55%;

    background:
        radial-gradient(
            circle at 35% 30%,
            #ffb1d2,
            #ed3b82 45%,
            #9e124f 100%
        );

    border:
        2px solid #ff8fbd;

    box-shadow:
        inset 0 4px 12px #ffffff55,
        0 4px 10px #8c104455;
}

.rose-flower span:nth-child(1) {
    transform:
        translateY(-24px)
        rotate(0deg);
}

.rose-flower span:nth-child(2) {
    transform:
        translate(23px,-8px)
        rotate(55deg);
}

.rose-flower span:nth-child(3) {
    transform:
        translate(15px,22px)
        rotate(110deg);
}

.rose-flower span:nth-child(4) {
    transform:
        translate(-15px,22px)
        rotate(160deg);
}

.rose-flower span:nth-child(5) {
    transform:
        translate(-23px,-8px)
        rotate(220deg);
}

.rose-flower span:nth-child(6) {
    transform:
        scale(.65);

    background:
        radial-gradient(
            circle,
            #ffd4e5,
            #d61e68 55%,
            #8b1047
        );

    z-index: 5;
}

@keyframes flowerSway {

    0%,100% {
        transform:
            rotate(-2deg);
    }

    50% {
        transform:
            rotate(3deg)
            translateY(-4px);
    }
}

.rose-stem {
    position: absolute;

    bottom: 47px;

    width: 10px;

    height: 125px;

    border-radius: 10px;

    background:
        linear-gradient(
            90deg,
            #145a35,
            #49a95e,
            #0c482b
        );

    z-index: 2;
}

.rose-leaf {
    position: absolute;

    width: 48px;
    height: 24px;

    background:
        linear-gradient(
            135deg,
            #6abd70,
            #155a35
        );

    border-radius:
        100% 0 100% 0;

    bottom: 110px;

    z-index: 3;
}

.leaf-left {
    left: 34px;

    transform:
        rotate(-25deg);
}

.leaf-right {
    right: 34px;

    transform:
        rotate(205deg);
}

.rose-card {
    padding: 8px 18px;

    border-radius: 25px;

    background:
        #ffffffaa;

    border:
        1px solid white;

    color: #9a165f;

    font-weight: 900;

    box-shadow:
        0 8px 25px #8c174655;

    backdrop-filter:
        blur(5px);

    z-index: 6;

    margin-bottom: 3px;
}

.rose-petal {
    position: absolute;

    top: -30px;

    font-size: 20px;

    z-index: 3;

    pointer-events: none;

    animation:
        petalFall linear forwards;
}

@keyframes petalFall {

    0% {
        transform:
            translateY(0)
            rotate(0deg);

        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    100% {
        transform:
            translateY(105vh)
            translateX(120px)
            rotate(600deg);

        opacity: 0;
    }
}


/* ============================================================
CAKE
============================================================ */

.cakearea {
    position: relative;

    width: min(520px, 95vw);

    height: 360px;

    z-index: 5;
}

.cake {
    position: absolute;

    left: 50%;
    bottom: 10px;

    width: 390px;
    height: 300px;

    transform:
        translateX(-50%);
}

.plate {
    position: absolute;

    bottom: 0;
    left: 10px;

    width: 370px;
    height: 28px;

    border-radius: 50%;

    background:
        linear-gradient(
            #fff,
            #dfb1cc
        );
}

.tier {
    position: absolute;

    border-radius:
        18px
        18px
        25px
        25px;

    background:
        linear-gradient(
            #fff7fb,
            #ef8fbd
        );

    border: 4px solid white;

    transition: 1s;
}

.t1 {
    width: 310px;
    height: 80px;

    bottom: 25px;
    left: 40px;
}

.t2 {
    width: 245px;
    height: 75px;

    bottom: 92px;
    left: 72px;
}

.t3 {
    width: 175px;
    height: 70px;

    bottom: 155px;
    left: 107px;
}

.frost {
    position: absolute;

    top: -12px;

    width: 100%;
    height: 27px;

    background: white;

    border-radius: 50%;
}

.ctitle {
    position: absolute;

    bottom: 118px;

    left: 50%;

    transform:
        translateX(-50%);

    color: #a52069;

    font-weight: 900;

    font-size: 15px;

    width: 230px;
}

.candle {
    position: absolute;

    bottom: 222px;

    width: 17px;
    height: 58px;

    background:
        repeating-linear-gradient(
            45deg,
            #ff4c94 0 7px,
            #fff 7px 14px
        );

    border-radius: 5px;
}

.c1 {
    left: 128px;
}

.c2 {
    left: 187px;
}

.c3 {
    left: 246px;
}

.flame {
    position: absolute;

    top: -29px;

    width: 19px;
    height: 29px;

    background:
        radial-gradient(
            circle at 50% 70%,
            #fff 0 18%,
            #ffe45f 30%,
            #ff711d 65%,
            transparent 70%
        );

    border-radius: 50%;

    animation:
        flame 0.5s infinite alternate;
}

.off {
    opacity: 0;

    transform:
        scale(0);
}

@keyframes flame {

    to {
        transform:
            rotate(5deg)
            scale(1.1);
    }
}


/* ============================================================
KNIFE
============================================================ */

.knife {
    position: absolute;

    right: 15px;
    top: 90px;

    width: 170px;
    height: 25px;

    opacity: 0;

    transform:
        rotate(-35deg)
        translate(100px, -40px);

    transition: 1.2s;
}

.knife.show {
    opacity: 1;

    transform:
        rotate(-35deg);
}

.blade {
    position: absolute;

    width: 125px;
    height: 18px;

    background:
        linear-gradient(
            #fff,
            #aeb5bf,
            #fff
        );

    clip-path:
        polygon(
            0 0,
            100% 0,
            86% 100%,
            0 100%
        );
}

.handle {
    position: absolute;

    right: 0;
    top: -2px;

    width: 58px;
    height: 24px;

    background:
        linear-gradient(
            #222,
            #080808
        );

    border-radius:
        5px
        12px
        12px
        5px;
}

.cutline {
    position: absolute;

    left: 50%;

    bottom: 80px;

    width: 5px;
    height: 130px;

    background: #c73575;

    transform:
        translateX(-50%)
        scaleY(0);

    transform-origin: bottom;

    transition: 0.8s;
}

.cutline.show {
    transform:
        translateX(-50%)
        scaleY(1);
}

.cut .t1 {
    transform:
        translateX(-18px);
}

.cut .t2 {
    transform:
        translateX(-14px);
}

.cut .t3 {
    transform:
        translateX(-10px);
}

.cuttext {
    color: #8f1558;

    font-weight: 900;

    font-size: 21px;

    opacity: 0;
}

.cuttext.show {
    animation:
        wish 0.7s forwards;
}


/* ============================================================
ROMANTIC FINALE
============================================================ */

#s12 {
    background:
        radial-gradient(
            circle at 50% 35%,
            #fffaff 0%,
            #ffd2e6 38%,
            #e27eaf 72%,
            #8d245f 100%
        );
}

.finale {
    position: relative;

    width: min(900px, 94vw);

    padding:
        28px 25px 25px;

    border-radius: 42px;

    background:
        linear-gradient(
            145deg,
            #ffffffc9,
            #fff0f8b8
        );

    border:
        2px solid #ffffff;

    box-shadow:
        0 30px 100px #7c164f55,
        inset 0 0 45px #ffffff80;

    backdrop-filter:
        blur(12px);

    z-index: 10;

    overflow: hidden;
}

.final-rings {
    position: absolute;

    width: 400px;
    height: 400px;

    border-radius: 50%;

    border:
        2px solid #ff5fa544;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%);

    animation:
        ringPulse 3s infinite;
}

.final-rings:after {
    content: "";

    position: absolute;

    inset: 35px;

    border-radius: 50%;

    border:
        2px solid #ff5fa533;
}

@keyframes ringPulse {

    50% {
        transform:
            translate(-50%, -50%)
            scale(1.08);

        opacity: .7;
    }
}

.final-heart {
    font-size:
        clamp(55px, 9vw, 100px);

    position: relative;

    z-index: 5;

    animation:
        finalHeart 1.2s infinite;

    filter:
        drop-shadow(
            0 0 25px #ff3e91
        );
}

@keyframes finalHeart {

    0%,100% {
        transform:
            scale(1);
    }

    50% {
        transform:
            scale(1.12);
    }
}

.final-title {
    position: relative;

    z-index: 5;

    color: #95155d;

    font-size:
        clamp(30px, 6vw, 68px);

    font-weight: 900;

    text-shadow:
        0 0 25px #ffffff;

    margin-top: 3px;
}

.final-subtitle {
    position: relative;

    z-index: 5;

    color: #76264f;

    font-size:
        clamp(16px, 2.2vw, 23px);

    line-height: 1.65;

    max-width: 700px;

    margin:
        10px auto 15px;
}

.final-lines {
    position: relative;

    z-index: 5;

    color: #8f1558;

    font-size:
        clamp(17px, 2.3vw, 25px);

    font-weight: 700;

    line-height: 1.75;
}

.final-highlight {
    position: relative;

    z-index: 5;

    margin:
        15px auto;

    color: #b3176d;

    font-size:
        clamp(21px, 3vw, 34px);

    font-weight: 900;

    text-shadow:
        0 0 20px #ff8fc744;
}

.final-sign {
    position: relative;

    z-index: 5;

    color: #68264d;

    font-size:
        clamp(15px, 2vw, 20px);

    font-style: italic;

    line-height: 1.6;

    margin-top: 8px;
}


/* ============================================================
LOVE METER
============================================================ */

.meter {
    width: min(560px, 88vw);

    margin:
        15px auto 8px;

    z-index: 10;

    position: relative;
}

.track {
    height: 24px;

    border-radius: 30px;

    background: #ffffff99;

    border: 2px solid white;

    overflow: hidden;
}

.fill {
    height: 100%;

    width: 0;

    border-radius: 30px;

    background:
        linear-gradient(
            90deg,
            #ff4b91,
            #b71970,
            #ffd86d
        );

    transition: 3s;
}

.num {
    color: #8c1558;

    font-size: 24px;

    font-weight: 900;

    margin-top: 8px;
}


/* ============================================================
REPLAY BUTTON
============================================================ */

.replay {
    position: relative;

    z-index: 20;

    border: 0;

    border-radius: 25px;

    padding:
        10px 22px;

    margin-top: 8px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #ff4b9b,
            #a51665
        );

    font-weight: 900;

    cursor: pointer;

    box-shadow:
        0 8px 25px #a5166555;

    transition: .3s;
}

.replay:hover {
    transform:
        translateY(-3px)
        scale(1.05);
}


/* ============================================================
FLOATING HEARTS
============================================================ */

.heart {
    position: absolute;

    bottom: -60px;

    z-index: 50;

    pointer-events: none;

    animation:
        heartfloat linear forwards;
}

@keyframes heartfloat {

    15% {
        opacity: 1;
    }

    to {
        transform:
            translateY(-110vh)
            rotate(360deg);

        opacity: 0;
    }
}


/* ============================================================
CONFETTI
============================================================ */

.confetti {
    position: absolute;

    top: -20px;

    width: 9px;
    height: 17px;

    z-index: 100;

    animation:
        fall 3.5s linear forwards;
}

@keyframes fall {

    to {
        transform:
            translateY(110vh)
            rotate(720deg);

        opacity: 0;
    }
}


/* ============================================================
MUSIC BAR
============================================================ */

.music {
    position: fixed;

    left: 50%;
    bottom: 12px;

    transform:
        translateX(-50%);

    width: min(570px, 94vw);

    padding:
        10px 13px;

    border-radius: 28px;

    background: #23071ff0;

    border:
        1px solid #ffffff55;

    color: white;

    z-index: 9999;

    box-shadow:
        0 10px 45px #0008;
}

.musicrow {
    display: flex;

    align-items: center;

    gap: 10px;
}

.musicicon {
    width: 42px;
    height: 42px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #ff4c9b,
            #a91668
        );
}

.musicinfo {
    flex: 1;

    text-align: left;
}

.musicname {
    font-size: 13px;

    font-weight: 900;
}

.status {
    font-size: 11px;

    opacity: 0.8;

    margin-top: 3px;
}

.volume {
    width: 70px;
}


/* ============================================================
MOBILE
============================================================ */

@media(max-width:700px) {

    .gifts {
        transform:
            scale(0.68);

        margin:
            -5px 0;
    }

    .gift-center-wish {
        margin-top:
            -25px;
    }

    .cakearea {
        transform:
            scale(0.72);

        transform-origin:
            top center;

        height: 280px;
    }

    .volume {
        display: none;
    }

    .couple {
        gap: 4px;
    }

    .rose-garden {
        gap: 0;

        transform:
            scale(.72);

        height: 280px;
    }

    .finale {
        padding:
            20px 15px;
    }

    .final-rings {
        width: 280px;
        height: 280px;
    }
}

</style>

</head>


<body>

<div id="app">

<div id="stars"></div>


<!-- ========================================================
OPEN SCREEN
======================================================== -->

<div id="open">

    <div class="openheart">
        🎂❤️
    </div>

    <div class="opentitle">
        A Birthday Surprise For My Jaan
    </div>

    <div class="openmsg">
        A little surprise made with all my love... 💕
        <br>
        Tap below and let our story begin. ✨
    </div>

    <button class="openbtn" id="openbtn">
        💖 Open My Surprise 💖
    </button>

</div>


<!-- ========================================================
SCENE 1
======================================================== -->

<section class="scene active" id="s1">

    <div class="kicker">
        A Little Surprise For You ✨
    </div>

    <div class="date">
        17 SEPTEMBER
    </div>

    <h1>
        Wait... ❤️
    </h1>

    <div class="msg">
        Something beautiful is waiting for you...
        <br>
        because today belongs to you, my love. 💕
    </div>

    <div
        class="date"
        id="count"
        style="font-size:90px;margin-top:15px"
    >
        3
    </div>

</section>


<!-- ========================================================
SCENE 2
======================================================== -->

<section class="scene" id="s2">

    <div class="kicker">
        17 September • 12:00 AM 🌙
    </div>

    <h1>
        Happy Birthday,<br>
        My Jaan ❤️
    </h1>

    <div class="msg">
        The clock struck 12...
        <br>
        and my first wish had to be for you. 💕
        <br><br>
        Today is all about the person
        who makes my heart smile. 🌸
    </div>

</section>


<!-- ========================================================
SCENE 3
======================================================== -->

<section class="scene light" id="s3">

    <h1>
        My Beautiful Wife ❤️
    </h1>

    <div class="photo">
        <img id="wife">
    </div>

    <div class="msg">
        The most beautiful part of my life is YOU. 🌸
        <br>
        My favorite smile. My favorite person. My favorite love. ❤️
    </div>

</section>


<!-- ========================================================
SCENE 4
======================================================== -->

<section class="scene light" id="s4">

    <h1>
        Forever Us ❤️
    </h1>

    <div class="couple">

        <div class="cp">
            <img id="wc">
        </div>

        <div class="heartbig">
            ❤️
        </div>

        <div class="cp">
            <img id="hc">
        </div>

    </div>

    <div class="msg">
        Two hearts. One beautiful story. Forever. ♾️
        <br>
        No matter where life takes us,
        I want to keep choosing you. ❤️
    </div>

</section>


<!-- ========================================================
SCENE 5
======================================================== -->

<section class="scene light" id="s5">

    <h1>
        Our Beautiful Memories 📸
    </h1>

    <div
        class="memory"
        id="memory"
    ></div>

    <div
        class="count"
        id="mc"
    >
        Memory 1
    </div>

    <div class="msg">
        Every picture holds a little piece of our story. ❤️
        <br>
        And every memory with you is one I want forever.
    </div>

</section>


<!-- ========================================================
SCENE 6
======================================================== -->

<section class="scene light" id="s6">

    <h1>
        Six Little Wishes 🎈
    </h1>

    <div class="balloonstage">

        <div class="balloon b1">
            <span>LOVE ❤️</span>
        </div>

        <div class="balloon b2">
            <span>JAAN 💕</span>
        </div>

        <div class="balloon b3">
            <span>FOREVER ♾️</span>
        </div>

        <div class="balloon b4">
            <span>HAPPINESS 🌸</span>
        </div>

        <div class="balloon b5">
            <span>SUCCESS ✨</span>
        </div>

        <div class="balloon b6">
            <span>MY LOVE 💖</span>
        </div>

    </div>

    <div
        class="wish"
        id="wish"
    ></div>

    <div
        class="wishdesc"
        id="wd"
    ></div>

</section>


<!-- ========================================================
SCENE 7
======================================================== -->

<section class="scene light" id="s7">

    <h1>
        A Letter For You 💌
    </h1>

    <div
        class="letter"
        id="letter"
    ></div>

</section>


<!-- ========================================================
SCENE 8
======================================================== -->

<section class="scene light" id="s8">

    <h1>
        Little Gifts From My Heart 🎁
    </h1>

    <div class="gifts">

        <div
            class="gift"
            data-wish="My Love ❤️"
            data-desc="You are the love I never want to live without."
        >
            <div class="lid"></div>
            <div class="box"></div>
            <div class="ribbon"></div>
            <div class="gift-spark">✨💖✨</div>

            <div class="gift-message">
                ❤️ My Love ❤️
            </div>
        </div>


        <div
            class="gift"
            data-wish="My Forever ♾️"
            data-desc="If I had one wish, it would be to spend every tomorrow with you."
        >
            <div class="lid"></div>
            <div class="box"></div>
            <div class="ribbon"></div>
            <div class="gift-spark">💫❤️💫</div>

            <div class="gift-message">
                ♾️ My Forever ♾️
            </div>
        </div>


        <div
            class="gift"
            data-wish="My Happiness 🌸"
            data-desc="Your smile is one of my favorite reasons to smile."
        >
            <div class="lid"></div>
            <div class="box"></div>
            <div class="ribbon"></div>
            <div class="gift-spark">🌸💕🌸</div>

            <div class="gift-message">
                🌸 My Happiness 🌸
            </div>
        </div>


        <div
            class="gift"
            data-wish="My Everything 💍"
            data-desc="The greatest gift life gave me is having you in my world."
        >
            <div class="lid"></div>
            <div class="box"></div>
            <div class="ribbon"></div>
            <div class="gift-spark">💎❤️💎</div>

            <div class="gift-message">
                💖 My Everything 💖
            </div>
        </div>

    </div>


    <div
        class="gift-center-wish"
        id="giftWish"
    ></div>

    <div
        class="gift-center-desc"
        id="giftDesc"
    ></div>

</section>


<!-- ========================================================
SCENE 9
======================================================== -->

<section class="scene light" id="s9">

    <div class="kicker">
        A Garden Made For My Rose 🌸
    </div>

    <h1>
        Roses For My Rose 🌹
    </h1>

    <div class="rose-garden">

        <div class="rose-item">

            <div class="rose-glow"></div>

            <div class="rose-flower">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="rose-stem"></div>

            <div class="rose-leaf leaf-left"></div>
            <div class="rose-leaf leaf-right"></div>

            <div class="rose-card">
                LOVE ❤️
            </div>

        </div>


        <div class="rose-item">

            <div class="rose-glow"></div>

            <div class="rose-flower">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="rose-stem"></div>

            <div class="rose-leaf leaf-left"></div>
            <div class="rose-leaf leaf-right"></div>

            <div class="rose-card">
                FOREVER ♾️
            </div>

        </div>


        <div class="rose-item">

            <div class="rose-glow"></div>

            <div class="rose-flower">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="rose-stem"></div>

            <div class="rose-leaf leaf-left"></div>
            <div class="rose-leaf leaf-right"></div>

            <div class="rose-card">
                HAPPINESS 🌸
            </div>

        </div>

    </div>

    <div class="msg">
        If I could, I would fill your whole world with roses...
        <br>
        because you deserve every beautiful thing. ❤️
    </div>

</section>


<!-- ========================================================
SCENE 10
======================================================== -->

<section class="scene light" id="s10">

    <h1>
        Make A Wish 🎂
    </h1>

    <div class="cakearea">

        <div
            class="cake"
            id="cake"
        >

            <div class="plate"></div>

            <div class="tier t1">
                <div class="frost"></div>
            </div>

            <div class="tier t2">
                <div class="frost"></div>
            </div>

            <div class="tier t3">
                <div class="frost"></div>
            </div>

            <div class="ctitle">
                HAPPY BIRTHDAY<br>
                MY JAAN ❤️
            </div>

            <div class="candle c1">
                <div class="flame"></div>
            </div>

            <div class="candle c2">
                <div class="flame"></div>
            </div>

            <div class="candle c3">
                <div class="flame"></div>
            </div>

            <div
                class="cutline"
                id="cutline"
            ></div>

        </div>


        <div
            class="knife"
            id="knife"
        >

            <div class="blade"></div>
            <div class="handle"></div>

        </div>

    </div>


    <div
        class="cuttext"
        id="cuttext"
    >
        🎂 Cake Cut For My Jaan! 🔪❤️
    </div>

    <div class="msg">
        Close your eyes... make a wish...
        <br>
        and remember that someone loves you endlessly. ✨❤️
    </div>

</section>


<!-- ========================================================
SCENE 11
======================================================== -->

<section class="scene light" id="s11">

    <div class="kicker">
        One Last Thing Before The Ending... 💕
    </div>

    <h1>
        My Favorite Person ❤️
    </h1>

    <div class="photo">
        <img id="final">
    </div>

    <div class="msg">
        I hope you always know how deeply you are loved. 💕
        <br>
        You are not just a part of my life...
        <br>
        you are one of the most beautiful parts of it. ❤️
    </div>

</section>


<!-- ========================================================
SCENE 12 — ROMANTIC ENDING
======================================================== -->

<section class="scene light" id="s12">

    <div class="finale">

        <div class="final-rings"></div>

        <div class="final-heart">
            ❤️
        </div>

        <div class="final-title">
            Forever With You
        </div>

        <div class="final-subtitle">
            If I could write one wish for your birthday,
            it would be simple:
            <br>
            <strong>
                I want to be there for every birthday,
                every smile, every dream,
                and every beautiful chapter of your life.
            </strong>
        </div>


        <div class="final-lines">

            My wife. ❤️<br>

            My love. 💕<br>

            My happiness. 🌸<br>

            My peace. 🕊️<br>

            My home. 🏡<br>

            My forever. ♾️

        </div>


        <div class="final-highlight">

            Happy Birthday, My Jaan 🎂❤️

        </div>


        <div class="final-subtitle">

            May this new year of your life bring you
            everything your beautiful heart deserves.
            <br><br>

            And if life gives me the choice again and again...
            <br>

            <strong>
                I will choose you. Every single time. ❤️
            </strong>

        </div>


        <div class="meter">

            <div
                style="
                color:#8c1558;
                font-size:20px;
                font-weight:900;
                margin-bottom:8px
                "
            >
                Our Love Meter ❤️
            </div>

            <div class="track">

                <div
                    class="fill"
                    id="fill"
                ></div>

            </div>

            <div
                class="num"
                id="num"
            >
                0% Love ❤️
            </div>

        </div>


        <div class="final-sign">

            Forever yours,<br>

            <strong>
                Your Loving Husband ❤️
            </strong>

            <br><br>

            "My favorite place will always be
            wherever I am with you." 💞

        </div>


        <button
            class="replay"
            id="replay"
        >
            ❤️ Replay Our Story
        </button>

    </div>

</section>


<!-- ========================================================
MUSIC PLAYER
======================================================== -->

<div class="music">

    <div class="musicrow">

        <div class="musicicon">
            🎵
        </div>

        <div class="musicinfo">

            <div class="musicname">
                Birthday Music ❤️
            </div>

            <div
                class="status"
                id="status"
            >
                Waiting to start...
            </div>

        </div>

        <button
            class="musicbtn"
            id="mb"
        >
            ▶ Play
        </button>

        <input
            class="volume"
            id="vol"
            type="range"
            min="0"
            max="1"
            step=".01"
            value=".4"
        >

    </div>

</div>


<audio
    id="audio"
    preload="auto"
    loop
    playsinline
></audio>


</div>


<script>

/* ============================================================
DATA FROM PYTHON
============================================================ */

const P = __PHOTOS__;
const W = __WIFE__;
const H = __HUSBAND__;
const M = __MUSIC__;


/* ============================================================
HELPERS
============================================================ */

const $ = x =>
    document.getElementById(x);

const wait = x =>
    new Promise(
        resolve =>
            setTimeout(resolve, x)
    );


function scene(n) {

    document
        .querySelectorAll(".scene")
        .forEach(x =>
            x.classList.remove("active")
        );

    const target =
        $("s" + n);

    if (target) {
        target.classList.add("active");
    }
}


/* ============================================================
IMAGES
============================================================ */

function put(id, src) {

    const element =
        $(id);

    if (element && src) {
        element.src = src;
    }
}

put("wife", W);
put("wc", W);
put("hc", H);

if (P.length) {
    put(
        "final",
        P[P.length - 1]
    );
}


/* ============================================================
STARS
============================================================ */

for (
    let i = 0;
    i < 80;
    i++
) {

    let star =
        document.createElement("div");

    star.className =
        "star";

    star.style.position =
        "absolute";

    star.style.width =
        Math.random() > .8
            ? "3px"
            : "2px";

    star.style.height =
        star.style.width;

    star.style.background =
        "white";

    star.style.borderRadius =
        "50%";

    star.style.left =
        Math.random() * 100 + "%";

    star.style.top =
        Math.random() * 100 + "%";

    star.style.opacity =
        0.25 +
        Math.random() * 0.75;

    star.style.boxShadow =
        "0 0 8px white";

    $("stars")
        .appendChild(star);
}


/* ============================================================
MEMORIES
============================================================ */

P.forEach(
    (p, i) => {

        let image =
            document.createElement("img");

        image.src = p;

        if (i === 0) {
            image.className = "on";
        }

        $("memory")
            .appendChild(image);
    }
);


let pi = 0;


function next() {

    let images =
        $("memory")
        .querySelectorAll("img");

    if (!images.length) {
        return;
    }

    images.forEach(
        x =>
            x.classList.remove("on")
    );

    pi =
        (pi + 1) %
        images.length;

    images[pi]
        .classList
        .add("on");

    $("mc").innerText =
        `Memory ${pi + 1} of ${images.length}`;
}


/* ============================================================
MUSIC
============================================================ */

const audio =
    $("audio");

const mb =
    $("mb");

const status =
    $("status");

const vol =
    $("vol");

if (M) {

    audio.src = M;

} else {

    status.innerText =
        "music.mp3 not found";
}


async function play() {

    if (!M) {
        return;
    }

    try {

        audio.volume =
            Number(
                vol.value
            );

        await audio.play();

        mb.innerText =
            "🔊 Playing";

        status.innerText =
            "Birthday music is playing ❤️";

    } catch (e) {

        status.innerText =
            "Tap Play to start music 🎵";
    }
}


mb.onclick = () => {

    if (audio.paused) {

        play();

    } else {

        audio.pause();

        mb.innerText =
            "▶ Play";

        status.innerText =
            "Music paused";
    }
};


vol.oninput = () => {

    audio.volume =
        Number(
            vol.value
        );
};


/* ============================================================
CONFETTI
============================================================ */

function confetti(n = 30) {

    let colors = [
        "#ff4c98",
        "#ffd45c",
        "#fff",
        "#b96ee7",
        "#ff8d76"
    ];

    for (
        let i = 0;
        i < n;
        i++
    ) {

        let p =
            document.createElement(
                "div"
            );

        p.className =
            "confetti";

        p.style.left =
            Math.random() * 100 +
            "%";

        p.style.background =
            colors[
                Math.floor(
                    Math.random() *
                    colors.length
                )
            ];

        p.style.animationDuration =
            2 +
            Math.random() * 2 +
            "s";

        $("app")
            .appendChild(p);

        setTimeout(
            () => p.remove(),
            4500
        );
    }
}


/* ============================================================
FLOATING HEARTS
============================================================ */

function hearts() {

    let h =
        document.createElement(
            "div"
        );

    h.className =
        "heart";

    h.innerText =
        [
            "❤️",
            "💕",
            "💗",
            "💖",
            "💘",
            "💞"
        ][
            Math.floor(
                Math.random() * 6
            )
        ];

    h.style.left =
        Math.random() * 100 +
        "%";

    h.style.fontSize =
        15 +
        Math.random() * 25 +
        "px";

    h.style.animationDuration =
        5 +
        Math.random() * 5 +
        "s";

    $("app")
        .appendChild(h);

    setTimeout(
        () => h.remove(),
        11000
    );
}


setInterval(
    hearts,
    500
);


/* ============================================================
BALLOONS
============================================================ */

async function balloons() {

    let b =
        document.querySelectorAll(
            ".balloon"
        );

    let wishes = [

        [
            "LOVE ❤️",
            "May our love keep growing every single day."
        ],

        [
            "JAAN 💕",
            "You will always be my most special person."
        ],

        [
            "FOREVER ♾️",
            "I want countless beautiful memories with you."
        ],

        [
            "HAPPINESS 🌸",
            "May your beautiful smile never disappear."
        ],

        [
            "SUCCESS ✨",
            "May every dream of yours come true."
        ],

        [
            "MY LOVE 💖",
            "Happy Birthday to the love of my life."
        ]

    ];


    for (
        let i = 0;
        i < b.length;
        i++
    ) {

        $("wish")
            .classList
            .remove("show");

        b[i]
            .classList
            .add("rise");

        await wait(1000);

        b[i]
            .classList
            .add("pop");

        await wait(250);

        $("wish").innerText =
            wishes[i][0];

        $("wd").innerText =
            wishes[i][1];

        $("wish")
            .classList
            .add("show");

        confetti(20);

        await wait(1400);
    }
}


/* ============================================================
ROMANTIC LETTER
============================================================ */

async function letter() {

    let text =
`My Jaan, ❤️

Today is your birthday,
but somehow I feel like I am the lucky one...

Because I get to have you in my life.

You are the person whose smile
can make an ordinary day feel special.

You are the person I want to tell
my little stories to,
share my happiest moments with,
and hold close when life gets difficult.

I may not always have the perfect words,
but there is one thing I will always know:

I love you.

I love your smile.
I love your little ways.
I love the happiness you bring into my life.
And most of all,
I love the feeling of knowing
that you are my person. ❤️

On your birthday,
I wish you more than just happiness.

I wish you peaceful mornings,
beautiful dreams,
successful days,
a heart that always feels loved,
and a life filled with reasons to smile.

And selfishly,
I wish that I get to be beside you
through all of it.

Through the good days.
Through the difficult days.
Through every birthday.
Through every new chapter.

If I could give you one gift
that would last forever,
I would give you my heart...

because it already belongs to you. ❤️

Happy Birthday, My Jaan. 🎂💕

May this new year of your life
be as beautiful as your heart.

And whenever you wonder
how much you mean to me,
just remember this:

You are not just someone I love.

You are my love.
My happiness.
My peace.
My home.

Forever yours. ❤️`;

    $("letter").innerText =
        "";

    for (
        let character of text
    ) {

        $("letter").innerText +=
            character;

        await wait(8);
    }
}


/* ============================================================
GIFTS
============================================================ */

async function giftSparkles(gift) {

    for (
        let i = 0;
        i < 12;
        i++
    ) {

        let s =
            document.createElement(
                "div"
            );

        s.innerText =
            [
                "❤️",
                "💕",
                "✨",
                "💖",
                "🌸"
            ][
                Math.floor(
                    Math.random() * 5
                )
            ];

        s.style.position =
            "absolute";

        s.style.left =
            gift.offsetLeft +
            40 +
            Math.random() * 40 +
            "px";

        s.style.top =
            gift.offsetTop +
            45 +
            "px";

        s.style.zIndex =
            "200";

        s.style.fontSize =
            "18px";

        s.style.pointerEvents =
            "none";

        s.style.transition =
            "1.2s ease-out";

        $("app")
            .appendChild(s);

        setTimeout(
            () => {

                s.style.transform =
                    `translate(
                        ${(Math.random() - .5) * 180}px,
                        ${-80 - Math.random() * 120}px
                    ) scale(1.4)`;

                s.style.opacity =
                    "0";

            },
            30
        );

        setTimeout(
            () => s.remove(),
            1400
        );
    }
}


async function gifts() {

    let giftList =
        document.querySelectorAll(
            ".gift"
        );

    for (
        let i = 0;
        i < giftList.length;
        i++
    ) {

        let gift =
            giftList[i];

        let wish =
            gift.dataset.wish;

        let desc =
            gift.dataset.desc;


        gift.classList
            .add("open");


        $("giftWish")
            .classList
            .remove("show");

        $("giftWish")
            .innerText =
            wish;

        $("giftDesc")
            .innerText =
            desc;


        await wait(450);


        $("giftWish")
            .classList
            .add("show");


        giftSparkles(gift);

        confetti(25);


        await wait(1700);
    }
}


/* ============================================================
ROSES
============================================================ */

function petals() {

    for (
        let i = 0;
        i < 28;
        i++
    ) {

        setTimeout(
            () => {

                let petal =
                    document.createElement(
                        "div"
                    );

                petal.className =
                    "rose-petal";

                petal.innerText =
                    [
                        "🌸",
                        "🌹",
                        "💗"
                    ][
                        Math.floor(
                            Math.random() * 3
                        )
                    ];

                petal.style.left =
                    Math.random() * 100 +
                    "%";

                petal.style.fontSize =
                    12 +
                    Math.random() * 18 +
                    "px";

                petal.style.animationDuration =
                    4 +
                    Math.random() * 5 +
                    "s";

                $("app")
                    .appendChild(petal);

                setTimeout(
                    () =>
                        petal.remove(),
                    10000
                );

            },
            i * 160
        );
    }
}


async function roses() {

    let roses =
        document.querySelectorAll(
            ".rose-item"
        );

    for (
        let i = 0;
        i < roses.length;
        i++
    ) {

        await wait(350);

        roses[i]
            .classList
            .add("bloom");
    }

    petals();

    await wait(1200);

    petals();
}


/* ============================================================
CAKE
============================================================ */

async function cakeShow() {

    await wait(1300);

    document
        .querySelectorAll(".flame")
        .forEach(
            x =>
                x.classList.add(
                    "off"
                )
        );

    await wait(700);

    $("knife")
        .classList
        .add("show");

    await wait(1200);

    $("cutline")
        .classList
        .add("show");

    $("cake")
        .classList
        .add("cut");

    $("cuttext")
        .classList
        .add("show");

    confetti(100);

    await wait(2200);
}


/* ============================================================
LOVE METER
============================================================ */

async function meter() {

    setTimeout(
        () => {

            $("fill")
                .style
                .width =
                "100%";

        },
        100
    );


    for (
        let n = 0;
        n <= 100;
        n++
    ) {

        $("num").innerText =
            n +
            "% Love ❤️";

        await wait(22);
    }
}


/* ============================================================
RESET
============================================================ */

function resetStory() {

    document
        .querySelectorAll(
            ".scene"
        )
        .forEach(
            x =>
                x.classList
                .remove("active")
        );


    $("s1")
        .classList
        .add("active");


    $("open")
        .classList
        .remove("hide");


    $("count")
        .innerText =
        "3";


    $("fill")
        .style
        .width =
        "0";


    $("num")
        .innerText =
        "0% Love ❤️";


    $("knife")
        .classList
        .remove("show");


    $("cutline")
        .classList
        .remove("show");


    $("cuttext")
        .classList
        .remove("show");


    $("cake")
        .classList
        .remove("cut");


    document
        .querySelectorAll(".flame")
        .forEach(
            x =>
                x.classList
                .remove("off")
        );


    document
        .querySelectorAll(".gift")
        .forEach(
            x =>
                x.classList
                .remove("open")
        );


    document
        .querySelectorAll(".rose-item")
        .forEach(
            x =>
                x.classList
                .remove("bloom")
        );


    $("giftWish")
        .innerText =
        "";

    $("giftDesc")
        .innerText =
        "";

    $("giftWish")
        .classList
        .remove("show");


    $("letter")
        .innerText =
        "";

    pi = 0;


    if (P.length) {

        let images =
            $("memory")
            .querySelectorAll(
                "img"
            );

        images.forEach(
            x =>
                x.classList
                .remove("on")
        );

        if (images[0]) {
            images[0]
                .classList
                .add("on");
        }

        $("mc")
            .innerText =
            "Memory 1";
    }


    window.scrollTo(
        0,
        0
    );
}


/* ============================================================
MAIN SHOW
============================================================ */

async function show() {

    scene(1);

    for (
        let n = 3;
        n > 0;
        n--
    ) {

        $("count")
            .innerText =
            n;

        await wait(650);
    }


    $("count")
        .innerText =
        "❤️";

    await wait(700);


    scene(2);

    confetti(40);

    await wait(3000);


    scene(3);

    await wait(3300);


    scene(4);

    await wait(3800);


    scene(5);

    pi = 0;

    let timer =
        setInterval(
            next,
            1900
        );

    await wait(
        Math.max(
            10000,
            P.length * 1900
        )
    );

    clearInterval(timer);


    scene(6);

    await balloons();


    scene(7);

    await letter();

    await wait(2200);


    scene(8);

    await gifts();

    await wait(1000);


    scene(9);

    await roses();

    await wait(3500);


    scene(10);

    await cakeShow();


    scene(11);

    await wait(3500);


    scene(12);

    await meter();

    confetti(180);

    petals();

    await wait(1000);

    petals();
}


/* ============================================================
OPEN BUTTON
============================================================ */

$("openbtn").onclick =
    async () => {

        await play();

        $("open")
            .classList
            .add("hide");

        setTimeout(
            show,
            400
        );
    };


/* ============================================================
REPLAY
============================================================ */

$("replay").onclick =
    async () => {

        resetStory();

        await wait(500);

        $("open")
            .classList
            .add("hide");

        await play();

        setTimeout(
            show,
            400
        );
    };

</script>

</body>
</html>
'''


# ============================================================
# REPLACE PYTHON PLACEHOLDERS
# ============================================================

html = (
    html
    .replace(
        "__PHOTOS__",
        photos_json
    )
    .replace(
        "__WIFE__",
        wife_json
    )
    .replace(
        "__HUSBAND__",
        husband_json
    )
    .replace(
        "__MUSIC__",
        music_json
    )
)


# ============================================================
# SHOW APP
# ============================================================

components.html(
    html,
    height=950,
    scrolling=False
)


# ============================================================
# MISSING ASSETS WARNING
# ============================================================

missing = []

if not wife:
    missing.append("Wife.png")

if not husband:
    missing.append("Husband.jpg")

if len(photos) < 8:
    missing.append(
        f"{8 - len(photos)} memory photo(s)"
    )

if not music:
    missing.append("music.mp3")


if missing:

    st.warning(
        "⚠️ Missing assets: "
        + ", ".join(missing)
    )