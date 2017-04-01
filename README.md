# Проект Open-Recycle  
Приложение-помощник, которое облегчает раздельный сбор, помогая людям сортировать бытовые отходы с помощью нейронных сетей  
  
**В данный момент проект не завершен, находится в стадии разработки.**  
  
classifier-api - REST API для работы с приложением   
open-recycle-android - Android клиент  
wastedataminer - Telegram бот 

# Руководство по развёртыванию back-end'а

1. Мы используем python3.4. Проект должен заработать с любым python3.
2. Установите Tensorflow 1.0.0+: https://www.tensorflow.org/install/install_linux#installing_with_virtualenv, https://www.tensorflow.org/versions/r0.10/get_started/os_setup#virtualenv_installation
3. Остальные зависимости: pip install -r requirements.txt
4. Скачайте датасет (https://mega.nz/#!1V5WxQLa!sUPWYKgWRrMsFpWTHHJCpCmYY3elFTEx1itaEykrrF8) или создайте свой.
5. Обучите нейросеть: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/image_retraining/retrain.py, retrain.py --image_dir $DATASET_DIR
6. Проверить работу: python classify.py $SOME_IMAGE_FILE. Пример вывода:
```
$ python classify.py /var/tmp/horse.jpg                                             
run_inference_on_image
/var/tmp/horse.jpg
5=====================================
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE3 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/framework/op_def_util.cc:332] Op BatchNormWithGlobalNormalization is deprecated. It will cease to work in GraphDef version 9. Use tf.nn.batch_normalization().
b'stupid photo\n' (score = 0.99434)
b'disposable paper cups resized\n' (score = 0.00194)
b'crumpled paper\n' (score = 0.00157)
b'lame foil\n' (score = 0.00081)
b'plastic bottle\n' (score = 0.00072)
```
7. Запустите back-end: python app.py 

