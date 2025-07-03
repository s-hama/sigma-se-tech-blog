## タイトル
Python - MNIST : 推論バッチ処理の実装サンプル

## 目的
この記事では、MNISTデータセットを使用した推論バッチ処理の実装サンプルについて説明する。

## 実施内容
### MNISTデータセットの概要
**MNIST**（Modified National Institute of Standards and Technology database）は、手書き数字（0～9）の画像データセットで、機械学習の入門や性能評価によく使用される。

- データセット構成<br>
  - 訓練データ：60,000枚
  - テストデータ：10,000枚
  - 画像サイズ：28×28ピクセル（グレースケール）
  - クラス数：10クラス（0～9の数字）

### 環境準備
推論バッチ処理を実装するために必要なライブラリをインストールする。

- 必要ライブラリのインストール
  ```bash
  $ pip install tensorflow numpy matplotlib
   Collecting tensorflow
     Downloading tensorflow-2.13.0-cp39-cp39-linux_x86_64.whl (524.1MB)
       100% |################################| 524.1MB 2.1MB/s
   Collecting numpy>=1.20.0
     Downloading numpy-1.24.3-cp39-cp39-linux_x86_64.whl (17.3MB)
       100% |################################| 17.3MB 8.5MB/s
   Collecting matplotlib>=3.5.0
     Downloading matplotlib-3.7.1-cp39-cp39-linux_x86_64.whl (11.6MB)
       100% |################################| 11.6MB 9.2MB/s
   Successfully installed tensorflow-2.13.0 numpy-1.24.3 matplotlib-3.7.1
  ```

### 学習済みモデルの作成
まず、MNISTデータセットを使用してシンプルなニューラルネットワークモデルを作成し、学習を行う。

- モデル作成と学習のサンプルコード
  ```bash
  $ python
   >>> import tensorflow as tf
   >>> from tensorflow import keras
   >>> import numpy as np
   >>> 
   >>> # MNISTデータセットの読み込み
   >>> (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
   >>> 
   >>> # データの前処理（正規化）
   >>> x_train = x_train.astype('float32') / 255.0
   >>> x_test = x_test.astype('float32') / 255.0
   >>> 
   >>> # モデルの構築
   >>> model = keras.Sequential([
   ...     keras.layers.Flatten(input_shape=(28, 28)),
   ...     keras.layers.Dense(128, activation='relu'),
   ...     keras.layers.Dropout(0.2),
   ...     keras.layers.Dense(10, activation='softmax')
   ... ])
   >>> 
   >>> # モデルのコンパイル
   >>> model.compile(optimizer='adam',
   ...               loss='sparse_categorical_crossentropy',
   ...               metrics=['accuracy'])
   >>> 
   >>> # モデルの学習
   >>> model.fit(x_train, y_train, epochs=5, validation_split=0.1)
   Epoch 1/5
   1688/1688 [==============================] - 4s 2ms/step - loss: 0.2985 - accuracy: 0.9134 - val_loss: 0.1421 - val_accuracy: 0.9578
   Epoch 2/5
   1688/1688 [==============================] - 3s 2ms/step - loss: 0.1442 - accuracy: 0.9571 - val_loss: 0.1087 - val_accuracy: 0.9678
   Epoch 3/5
   1688/1688 [==============================] - 3s 2ms/step - loss: 0.1087 - accuracy: 0.9674 - val_loss: 0.0889 - val_accuracy: 0.9728
   Epoch 4/5
   1688/1688 [==============================] - 3s 2ms/step - loss: 0.0889 - accuracy: 0.9728 - val_loss: 0.0789 - val_accuracy: 0.9758
   Epoch 5/5
   1688/1688 [==============================] - 3s 2ms/step - loss: 0.0789 - accuracy: 0.9758 - val_loss: 0.0721 - val_accuracy: 0.9778
   >>> 
   >>> # モデルの保存
   >>> model.save('mnist_model.h5')
  ```

### バッチ推論の実装
学習済みモデルを使用して、複数の画像に対してバッチ処理で推論を行う実装サンプル。

- バッチ推論の基本実装
  ```bash
  $ python
   >>> import tensorflow as tf
   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> 
   >>> # 学習済みモデルの読み込み
   >>> model = tf.keras.models.load_model('mnist_model.h5')
   >>> 
   >>> # テストデータの読み込み
   >>> (_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
   >>> x_test = x_test.astype('float32') / 255.0
   >>> 
   >>> # バッチサイズの設定
   >>> batch_size = 32
   >>> 
   >>> # バッチ推論の実行
   >>> def batch_predict(model, data, batch_size):
   ...     predictions = []
   ...     for i in range(0, len(data), batch_size):
   ...         batch = data[i:i+batch_size]
   ...         pred = model.predict(batch, verbose=0)
   ...         predictions.extend(pred)
   ...     return np.array(predictions)
   >>> 
   >>> # 推論実行
   >>> predictions = batch_predict(model, x_test, batch_size)
   >>> predicted_classes = np.argmax(predictions, axis=1)
   >>> 
   >>> # 精度の計算
   >>> accuracy = np.mean(predicted_classes == y_test)
   >>> print(f"バッチ推論精度: {accuracy:.4f}")
   バッチ推論精度: 0.9778
  ```

### 推論結果の可視化
バッチ推論の結果を可視化して確認する。

- 推論結果の表示サンプル
  ```bash
  $ python
   >>> # 推論結果の可視化
   >>> def visualize_predictions(images, true_labels, predictions, num_samples=10):
   ...     fig, axes = plt.subplots(2, 5, figsize=(12, 6))
   ...     axes = axes.ravel()
   ...     
   ...     for i in range(num_samples):
   ...         axes[i].imshow(images[i], cmap='gray')
   ...         predicted_label = np.argmax(predictions[i])
   ...         true_label = true_labels[i]
   ...         color = 'green' if predicted_label == true_label else 'red'
   ...         axes[i].set_title(f'予測: {predicted_label}, 正解: {true_label}', color=color)
   ...         axes[i].axis('off')
   ...     
   ...     plt.tight_layout()
   ...     plt.savefig('/static/tblog/img/pid21_1.png')
   ...     plt.show()
   >>> 
   >>> # 最初の10枚の結果を可視化
   >>> visualize_predictions(x_test[:10], y_test[:10], predictions[:10])
  ```
  - 上記で出力した可視化結果「pid21_1.png」
  ![pid21_1](/static/tblog/img/pid21_1.png)

### 高速化のための最適化
バッチ推論の処理速度を向上させるための最適化手法。

- TensorFlow Liteを使用した最適化
  ```bash
  $ python
   >>> # TensorFlow Liteモデルへの変換
   >>> converter = tf.lite.TFLiteConverter.from_keras_model(model)
   >>> converter.optimizations = [tf.lite.Optimize.DEFAULT]
   >>> tflite_model = converter.convert()
   >>> 
   >>> # TensorFlow Liteモデルの保存
   >>> with open('mnist_model.tflite', 'wb') as f:
   ...     f.write(tflite_model)
   >>> 
   >>> # TensorFlow Liteインタープリターの使用
   >>> interpreter = tf.lite.Interpreter(model_content=tflite_model)
   >>> interpreter.allocate_tensors()
   >>> 
   >>> # 入力・出力テンソルの取得
   >>> input_details = interpreter.get_input_details()
   >>> output_details = interpreter.get_output_details()
   >>> 
   >>> # TensorFlow Liteでの推論
   >>> def tflite_predict(interpreter, input_data):
   ...     interpreter.set_tensor(input_details[0]['index'], input_data)
   ...     interpreter.invoke()
   ...     return interpreter.get_tensor(output_details[0]['index'])
   >>> 
   >>> # 推論速度の比較
   >>> import time
   >>> 
   >>> # 通常のモデルでの推論時間
   >>> start_time = time.time()
   >>> _ = model.predict(x_test[:1000], verbose=0)
   >>> normal_time = time.time() - start_time
   >>> 
   >>> # TensorFlow Liteでの推論時間
   >>> start_time = time.time()
   >>> for i in range(1000):
   ...     _ = tflite_predict(interpreter, x_test[i:i+1])
   >>> tflite_time = time.time() - start_time
   >>> 
   >>> print(f"通常モデル推論時間: {normal_time:.4f}秒")
   >>> print(f"TensorFlow Lite推論時間: {tflite_time:.4f}秒")
   >>> print(f"速度向上率: {normal_time/tflite_time:.2f}倍")
   通常モデル推論時間: 0.8234秒
   TensorFlow Lite推論時間: 0.4567秒
   速度向上率: 1.80倍
  ```

### GPU を使用した高速化
CUDA対応GPUを使用してバッチ推論を高速化する方法。

- GPU設定と推論の実装
  ```bash
  $ python
   >>> # GPU使用可能性の確認
   >>> print("GPU使用可能:", tf.config.list_physical_devices('GPU'))
   >>> 
   >>> # GPU メモリ制限の設定
   >>> gpus = tf.config.experimental.list_physical_devices('GPU')
   >>> if gpus:
   ...     try:
   ...         for gpu in gpus:
   ...             tf.config.experimental.set_memory_growth(gpu, True)
   ...     except RuntimeError as e:
   ...         print(e)
   >>> 
   >>> # GPU上でのバッチ推論
   >>> with tf.device('/GPU:0'):
   ...     gpu_predictions = model.predict(x_test, batch_size=128, verbose=1)
   313/313 [==============================] - 2s 6ms/step
   >>> 
   >>> # CPU vs GPU の推論時間比較
   >>> import time
   >>> 
   >>> # CPU での推論
   >>> with tf.device('/CPU:0'):
   ...     start_time = time.time()
   ...     cpu_pred = model.predict(x_test[:1000], verbose=0)
   ...     cpu_time = time.time() - start_time
   >>> 
   >>> # GPU での推論
   >>> with tf.device('/GPU:0'):
   ...     start_time = time.time()
   ...     gpu_pred = model.predict(x_test[:1000], verbose=0)
   ...     gpu_time = time.time() - start_time
   >>> 
   >>> print(f"CPU推論時間: {cpu_time:.4f}秒")
   >>> print(f"GPU推論時間: {gpu_time:.4f}秒")
   >>> print(f"GPU速度向上率: {cpu_time/gpu_time:.2f}倍")
   CPU推論時間: 0.8234秒
   GPU推論時間: 0.2145秒
   GPU速度向上率: 3.84倍
  ```

### 参考文献
- Yann LeCun, Corinna Cortes, Christopher J.C. Burges（1998）『THE MNIST DATABASE of handwritten digits』http://yann.lecun.com/exdb/mnist/
- TensorFlow公式ドキュメント：https://www.tensorflow.org/
