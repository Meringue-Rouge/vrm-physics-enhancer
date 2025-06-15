# vrm-physics-enhancer

### VRoid Studioで作成されたVRM 1.0モデルのフィジックスを改善するための様々なツール群です。

### A suite of various tools to improve the physics of VRM 1.0 models made with VRoid Studio.

![image](https://github.com/user-attachments/assets/1fa961bb-986f-4a5a-9bfe-f4adaf80426b)

## 特徴
- 胸と手のコライダー： 胸と手にコライダーを追加し、髪の毛の相互作用を良くし、いくつかのクリッピングを回避。
- 胸の物理調整： ジグル物理にジグルの増減を追加し、バストの2_端のボーンにウェイトを適用。
- ロングドレスの物理調整： 一般的にVRoidがデザインしたものより長いロングドレスの物理を調整し、より許容できるようにします。
- 物理を使ったモデルのスケール： より多くの物理演算をそのままにモデルを拡大縮小します。 これは1:1変換ではありませんが、十分に近いです。
- 追加ジグル・フィジックス (BETA)： 様々なボーンにジグル物理を追加。 走行距離は大きく異なり、しばしば醜い見た目の結果につながります。

## Features
- Breast/Hand Colliders: Adds colliders to the breasts and hands so that hair interacts better, and avoids some clipping.
- Breast Physics Tweaker: Adds more/less jiggle to the jiggle physics and applies weight to the 2_end bones of the bust.
- Long Dress Physics Tweaker: Adjusts the physics on long dresses that are generally longer than what VRoid was designed for, and makes them more tolerable.
- Model Scale with Physics: Scale the model while retaining more of the physics intact. This isn't a 1:1 conversion but it's close enough.
- Additional Jiggle Physics (BETA): Add jiggle physics to various bones. Your mileage will vary greatly, and often leads to ugly looking results.

## 使い方
- Blenderアドオンをインストールします。
- [VRM Addon for Blender](https://vrm-addon-for-blender.info/en/)がインストールされていることと、VRoid StudioのVRM 1.0モデルがあることを確認してください。
- [VRM Addon for Blender](https://vrm-addon-for-blender.info/en/)でVRMモデルをインポートします。
- Nを押してアドオンのタブのサイドパネルを開き、VRM Physics Enhancerタブを見つけます。
- 必要なオプションを適用し、モデルをVRMとしてエクスポートします。 オプションにカーソルを合わせると、それぞれの機能が何をするのかが表示されます。

## Usage
- Install the Blender addon.
- Make sure you have the [VRM Addon for Blender](https://vrm-addon-for-blender.info/en/) installed, and that you have a VRM 1.0 model from VRoid Studio.
- Import your VRM model with the [VRM Addon for Blender](https://vrm-addon-for-blender.info/en/).
- Press N to open the side panel of tabs with your addons, and find the VRM Physics Enhancer tab.
- Apply whatever options you need, and then export your model as a VRM. Hovering over options shows what each function does.
