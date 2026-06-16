"""
Sweet Land Adventure - Buildbox Classic 2.x .bbdoc generator
.bbdoc = ZIP archive containing project.xml + assets/
"""
import zipfile, os, shutil, uuid
from pathlib import Path

OUT_DIR  = Path("/sessions/keen-sweet-fermi/mnt/outputs")
ASSET_DIR = OUT_DIR / "sweet_land_assets"
PROJECT_NAME = "SweetLandAdventure"
BBDOC_PATH = OUT_DIR / f"{PROJECT_NAME}.bbdoc"

# ── Helper: unique ID
def uid(): return str(uuid.uuid4()).upper()

# ── Asset list (name → filename)
ASSETS = {
    "cookie_idle":          "cookie_idle.png",
    "cookie_run1":          "cookie_run1.png",
    "cookie_run2":          "cookie_run2.png",
    "cookie_run3":          "cookie_run3.png",
    "cookie_run4":          "cookie_run4.png",
    "cookie_jump":          "cookie_jump.png",
    "enemy_donut":          "enemy_donut.png",
    "enemy_lollipop":       "enemy_lollipop_fairy.png",
    "enemy_caramel":        "enemy_caramel_blob.png",
    "tile_cookie":          "tile_cookie_platform.png",
    "tile_marshmallow":     "tile_marshmallow.png",
    "tile_cotton":          "tile_cotton_candy.png",
    "tile_item_block":      "tile_item_block.png",
    "item_coin":            "item_candy_coin.png",
    "item_star":            "item_sugar_star.png",
    "item_cake":            "item_cake_slice.png",
    "item_rainbow":         "item_rainbow_candy.png",
    "ui_heart_full":        "ui_heart_full.png",
    "ui_heart_empty":       "ui_heart_empty.png",
    "prop_cupcake_house":   "prop_cupcake_house.png",
    "prop_lollipop_tree":   "prop_lollipop_tree.png",
    "prop_goal_flag":       "prop_goal_flag.png",
    "bg_cloud":             "bg_cloud.png",
    "bg_cotton_tree":       "bg_cotton_tree.png",
}

# ── IDs
IDS = {k: uid() for k in ASSETS}
CHAR_ID    = uid()
WORLD1_ID  = uid()
SCENE1_ID  = uid()
SCENE2_ID  = uid()
SCENE3_ID  = uid()
SCENE4_ID  = uid()
ANIM_IDLE_ID  = uid()
ANIM_RUN_ID   = uid()
ANIM_JUMP_ID  = uid()

# ── project.xml ──────────────────────────────────────────────────────────────
XML = f'''<?xml version="1.0" encoding="UTF-8"?>
<BuildBox version="2.3.8" projectName="{PROJECT_NAME}">
  <Game id="{uid()}" name="{PROJECT_NAME}" orientation="landscape"
        screenWidth="384" screenHeight="216"
        gravity="-20" backgroundColor="7DD8C6FF"
        startScene="{SCENE1_ID}">

    <!-- ═══ ANIMATIONS ══════════════════════════════════════════════ -->
    <Animations>

      <Animation id="{ANIM_IDLE_ID}" name="Idle" fps="4" loop="true">
        <Frame image="assets/{ASSETS["cookie_idle"]}" duration="0.25"/>
      </Animation>

      <Animation id="{ANIM_RUN_ID}" name="Run" fps="8" loop="true">
        <Frame image="assets/{ASSETS["cookie_run1"]}" duration="0.125"/>
        <Frame image="assets/{ASSETS["cookie_run2"]}" duration="0.125"/>
        <Frame image="assets/{ASSETS["cookie_run3"]}" duration="0.125"/>
        <Frame image="assets/{ASSETS["cookie_run4"]}" duration="0.125"/>
      </Animation>

      <Animation id="{ANIM_JUMP_ID}" name="Jump" fps="6" loop="false">
        <Frame image="assets/{ASSETS["cookie_jump"]}" duration="0.167"/>
      </Animation>

    </Animations>

    <!-- ═══ CHARACTER ════════════════════════════════════════════════ -->
    <Characters>
      <Character id="{CHAR_ID}" name="Cookie"
                 width="32" height="32"
                 speed="250" jumpForce="500"
                 maxHealth="5" lives="3"
                 gravityScale="1.0"
                 idleAnimation="{ANIM_IDLE_ID}"
                 runAnimation="{ANIM_RUN_ID}"
                 jumpAnimation="{ANIM_JUMP_ID}"
                 colliderType="box"
                 colliderOffsetX="0" colliderOffsetY="0"
                 colliderWidth="28" colliderHeight="30"/>
    </Characters>

    <!-- ═══ WORLDS ═══════════════════════════════════════════════════ -->
    <Worlds>

      <!-- ─── WORLD 1: 컵케이크 마을 ────────────────────────────── -->
      <World id="{WORLD1_ID}" name="W1 컵케이크 마을"
             backgroundColorTop="7DD8C6FF" backgroundColorBottom="FAD5B5FF"
             musicVolume="1.0" soundVolume="1.0">

        <Scenes>

          <!-- ── SCENE 1-1 ─────────────────────────────────────── -->
          <Scene id="{SCENE1_ID}" name="1-1 쿠키 마을 입구"
                 width="1920" height="216"
                 scrollType="horizontal"
                 characterId="{CHAR_ID}"
                 characterStartX="80" characterStartY="100"
                 nextScene="{SCENE2_ID}"
                 timeLimit="300">

            <!-- Background clouds -->
            <Object type="background" id="{uid()}" name="Cloud_1"
                    image="assets/{ASSETS["bg_cloud"]}"
                    x="200" y="160" width="128" height="80"
                    scrollSpeedX="0.3" layer="-2" tile="true"/>
            <Object type="background" id="{uid()}" name="Cloud_2"
                    image="assets/{ASSETS["bg_cloud"]}"
                    x="600" y="180" width="128" height="80"
                    scrollSpeedX="0.3" layer="-2" tile="true"/>
            <Object type="background" id="{uid()}" name="Cloud_3"
                    image="assets/{ASSETS["bg_cloud"]}"
                    x="1100" y="150" width="128" height="80"
                    scrollSpeedX="0.3" layer="-2" tile="true"/>

            <!-- Ground platforms (cookie tiles) -->
            <Object type="platform" id="{uid()}" name="Ground_Main"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="0" y="32" width="1920" height="64"
                    solid="true" tile="true" layer="0"/>

            <!-- Floating platforms -->
            <Object type="platform" id="{uid()}" name="Platform_1"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="250" y="112" width="128" height="32"
                    solid="true" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_2"
                    image="assets/{ASSETS["tile_marshmallow"]}"
                    x="450" y="144" width="96" height="32"
                    solid="true" bouncy="true" bounceForce="600" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_3"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="650" y="128" width="128" height="32"
                    solid="true" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_4"
                    image="assets/{ASSETS["tile_cotton"]}"
                    x="850" y="112" width="96" height="32"
                    solid="true" disappear="true" disappearTime="3.0" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_5"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="1050" y="144" width="160" height="32"
                    solid="true" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_6"
                    image="assets/{ASSETS["tile_marshmallow"]}"
                    x="1300" y="128" width="96" height="32"
                    solid="true" bouncy="true" bounceForce="600" layer="0"/>
            <Object type="platform" id="{uid()}" name="Platform_7"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="1500" y="112" width="192" height="32"
                    solid="true" layer="0"/>

            <!-- Item blocks -->
            <Object type="itemBlock" id="{uid()}" name="ItemBlock_1"
                    image="assets/{ASSETS["tile_item_block"]}"
                    x="320" y="144" width="64" height="64"
                    reward="coin" rewardCount="3" layer="1"/>
            <Object type="itemBlock" id="{uid()}" name="ItemBlock_2"
                    image="assets/{ASSETS["tile_item_block"]}"
                    x="720" y="160" width="64" height="64"
                    reward="cake" rewardCount="1" layer="1"/>
            <Object type="itemBlock" id="{uid()}" name="ItemBlock_Star"
                    image="assets/{ASSETS["tile_item_block"]}"
                    x="1100" y="176" width="64" height="64"
                    reward="rainbow" rewardCount="1" layer="1"/>

            <!-- Coins scattered -->
            <Object type="collectible" id="{uid()}" name="Coin_1"
                    image="assets/{ASSETS["item_coin"]}"
                    x="200" y="120" width="32" height="32"
                    value="100" layer="1"/>
            <Object type="collectible" id="{uid()}" name="Coin_2"
                    image="assets/{ASSETS["item_coin"]}"
                    x="232" y="120" width="32" height="32"
                    value="100" layer="1"/>
            <Object type="collectible" id="{uid()}" name="Coin_3"
                    image="assets/{ASSETS["item_coin"]}"
                    x="264" y="120" width="32" height="32"
                    value="100" layer="1"/>
            <Object type="collectible" id="{uid()}" name="SugarStar_1"
                    image="assets/{ASSETS["item_star"]}"
                    x="500" y="180" width="32" height="32"
                    value="1000" tag="star" layer="1"/>
            <Object type="collectible" id="{uid()}" name="Coin_Row2_1"
                    image="assets/{ASSETS["item_coin"]}"
                    x="900" y="128" width="32" height="32" value="100" layer="1"/>
            <Object type="collectible" id="{uid()}" name="Coin_Row2_2"
                    image="assets/{ASSETS["item_coin"]}"
                    x="932" y="128" width="32" height="32" value="100" layer="1"/>
            <Object type="collectible" id="{uid()}" name="Coin_Row2_3"
                    image="assets/{ASSETS["item_coin"]}"
                    x="964" y="128" width="32" height="32" value="100" layer="1"/>

            <!-- Enemies -->
            <Object type="enemy" id="{uid()}" name="Donut_1"
                    image="assets/{ASSETS["enemy_donut"]}"
                    x="400" y="64" width="64" height="64"
                    patrolLeft="350" patrolRight="550"
                    speed="80" damage="1" killOnJump="true" layer="1"/>
            <Object type="enemy" id="{uid()}" name="Donut_2"
                    image="assets/{ASSETS["enemy_donut"]}"
                    x="1000" y="64" width="64" height="64"
                    patrolLeft="950" patrolRight="1150"
                    speed="80" damage="1" killOnJump="true" layer="1"/>

            <!-- Props -->
            <Object type="decoration" id="{uid()}" name="LollipopTree_1"
                    image="assets/{ASSETS["prop_lollipop_tree"]}"
                    x="150" y="64" width="128" height="224" layer="-1"/>
            <Object type="decoration" id="{uid()}" name="LollipopTree_2"
                    image="assets/{ASSETS["prop_lollipop_tree"]}"
                    x="1400" y="64" width="128" height="224" layer="-1"/>
            <Object type="decoration" id="{uid()}" name="CottonTree_1"
                    image="assets/{ASSETS["bg_cotton_tree"]}"
                    x="750" y="64" width="96" height="160" layer="-1"/>

            <!-- Goal flag -->
            <Object type="goal" id="{uid()}" name="GoalFlag"
                    image="assets/{ASSETS["prop_goal_flag"]}"
                    x="1820" y="32" width="64" height="192"
                    triggerNextScene="true" layer="1"/>

            <!-- HUD elements -->
            <HUD>
              <Element type="lives" id="{uid()}"
                       imageFull="assets/{ASSETS["ui_heart_full"]}"
                       imageEmpty="assets/{ASSETS["ui_heart_empty"]}"
                       x="16" y="16" spacing="20" maxCount="5"/>
              <Element type="score" id="{uid()}"
                       x="192" y="16" fontSize="16"
                       color="FFFFFFFF" align="center"/>
              <Element type="coins" id="{uid()}"
                       image="assets/{ASSETS["item_coin"]}"
                       x="340" y="16" fontSize="14"
                       color="FFD700FF" align="right"/>
            </HUD>

          </Scene>

          <!-- ── SCENE 1-2 placeholder ─────────────────────────── -->
          <Scene id="{SCENE2_ID}" name="1-2 초콜릿 강"
                 width="1920" height="216"
                 scrollType="horizontal"
                 characterId="{CHAR_ID}"
                 characterStartX="80" characterStartY="100"
                 nextScene="{SCENE3_ID}"
                 timeLimit="300">
            <Object type="platform" id="{uid()}" name="Ground"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="0" y="32" width="1920" height="64"
                    solid="true" tile="true" layer="0"/>
            <Object type="goal" id="{uid()}" name="GoalFlag"
                    image="assets/{ASSETS["prop_goal_flag"]}"
                    x="1820" y="32" width="64" height="192"
                    triggerNextScene="true" layer="1"/>
          </Scene>

          <!-- ── SCENE 1-3 placeholder ─────────────────────────── -->
          <Scene id="{SCENE3_ID}" name="1-3 쿠키 숲길"
                 width="1920" height="216"
                 scrollType="horizontal"
                 characterId="{CHAR_ID}"
                 characterStartX="80" characterStartY="100"
                 nextScene="{SCENE4_ID}"
                 timeLimit="300">
            <Object type="platform" id="{uid()}" name="Ground"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="0" y="32" width="1920" height="64"
                    solid="true" tile="true" layer="0"/>
            <Object type="goal" id="{uid()}" name="GoalFlag"
                    image="assets/{ASSETS["prop_goal_flag"]}"
                    x="1820" y="32" width="64" height="192"
                    triggerNextScene="true" layer="1"/>
          </Scene>

          <!-- ── SCENE 1-4 Boss ────────────────────────────────── -->
          <Scene id="{SCENE4_ID}" name="1-4 미니보스 컵케이크 저택"
                 width="1920" height="216"
                 scrollType="horizontal"
                 characterId="{CHAR_ID}"
                 characterStartX="80" characterStartY="100"
                 nextScene="" timeLimit="0">
            <Object type="platform" id="{uid()}" name="Ground"
                    image="assets/{ASSETS["tile_cookie"]}"
                    x="0" y="32" width="1920" height="64"
                    solid="true" tile="true" layer="0"/>
            <Object type="decoration" id="{uid()}" name="CupcakeHouse"
                    image="assets/{ASSETS["prop_cupcake_house"]}"
                    x="800" y="32" width="192" height="256" layer="0"/>
            <Object type="enemy" id="{uid()}" name="Caramel_Boss"
                    image="assets/{ASSETS["enemy_caramel"]}"
                    x="900" y="64" width="80" height="80"
                    health="3" damage="1" boss="true"
                    patrolLeft="700" patrolRight="1100"
                    speed="60" killOnJump="true" layer="1"/>
          </Scene>

        </Scenes>
      </World>

    </Worlds>

    <!-- ═══ PHYSICS SETTINGS ════════════════════════════════════════ -->
    <Physics gravity="-20" airResistance="0.95" friction="0.85"/>

    <!-- ═══ AUDIO ═══════════════════════════════════════════════════ -->
    <Audio>
      <BGM file="" loop="true" volume="0.8"/>
      <SFX name="coin_collect"  file="" volume="1.0"/>
      <SFX name="jump"          file="" volume="1.0"/>
      <SFX name="enemy_defeat"  file="" volume="1.0"/>
      <SFX name="player_hurt"   file="" volume="1.0"/>
      <SFX name="level_clear"   file="" volume="1.0"/>
    </Audio>

    <!-- ═══ STORE / SCORE ═══════════════════════════════════════════ -->
    <Score highScoreEnabled="true" leaderboardEnabled="false"/>

  </Game>
</BuildBox>
'''

# ── Build .bbdoc (ZIP) ────────────────────────────────────────────────────────
print("📦 .bbdoc 패키징 중...")
with zipfile.ZipFile(BBDOC_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
    # project.xml
    zf.writestr("project.xml", XML)
    # embed all asset PNGs
    for key, filename in ASSETS.items():
        src = ASSET_DIR / filename
        if src.exists():
            zf.write(src, f"assets/{filename}")
            print(f"  + assets/{filename}")
        else:
            print(f"  ! Missing: {filename}")

size_kb = BBDOC_PATH.stat().st_size // 1024
print(f"\n✅ {BBDOC_PATH.name}  ({size_kb} KB)")
print(f"   경로: {BBDOC_PATH}")
