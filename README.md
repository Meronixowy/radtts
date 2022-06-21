# Flow-based TTS with Robust Alignment Learning, Diverse Synthesis, and Generative Modelling and Fine-Grained Control over of Low Dimensional (F0 and Energy) Speech Attributes.
This repository contains the source code and several checkpoints for our work based on our RADTTS model. RADTTS is a normalizing-flow-based TTS framework with high acoustic fidelity and a highly robust audio-transcription alignment module. Our project page and some samples can be found [here](https://nv-adlr.github.io/RADTTS), with relevant works listed [here](#relevant-papers).

This repository can be used to train the following models:

- A normalizing-flow bipartite architecture for mapping text to mel spectrograms
- A variant of the above, conditioned on F0 and Energy
- Normalizing flow models for explicitly modeling text-conditional phoneme duration, fundamental frequency (F0), and energy
- A standalone alignment module for learning unspervised text-audio alignments necessary for TTS training

We provide a link to a pre-trained HiFi-GAN model to perform vocoding.

## Setup
1. Clone this repo: `git clone https://github.com/NVIDIA/RADTTS.git`
2. Install python requirements or build docker image
    - Install python requirements: `pip install -r requirements.txt`
3. Update the filelists inside the filelists folder and json configs to point to your data
4. Download the pre-trained HiFi-GAN model to perform vocoding and update HiFi-GAN paths in the json config files

## Training RADTTS (without pitch and energy conditioning)
1. Train the decoder <br> 
	`python train.py -c config_ljs_radtts.json -p train_config.output_directory=outdir`
2. Further train with the duration predictor
	`python train.py -c config_ljs_radtts.json -p train_config.output_directory=outdir_wdur train_config.warmstart_checkpoint_path=model_path.pt model_config.include_modules="decatndur"`


## Training RADTTS++ (with pitch and energy conditioning)
1. Train the decoder<br> 
	`python train.py -c config_ljs_decoder.json -p train_config.output_directory=outdir`
2. Train the attribute predictor: autoregressive flow (agap), bi-partite flow (bgap) or deterministic (dap)<br>
    `python train.py -c config_ljs_{agap,bgap,dap}.json -p train_config.output_directory=outdir_wattr train_config.warmstart_checkpoint_path=model_path.pt`


## Training starting from a pre-trained model
1. Download our published [RADTTS LJS] or [RADTTS LibriTTS] model
2. `python train.py -c config.json -p train_config.ignore_layers=["speaker_embedding.weight"] train_config.checkpoint_path=model_path.pt`

## Multi-GPU (distributed)
1. `python -m torch.distributed.launch --use_env --nproc_per_node=NUM_GPUS_YOU_HAVE train.py -c config.json -p train_config.output_directory=outdir`

## Inference demo

1. `python inference.py -c CONFIG_PATH -r RADTTS_PATH -v HG_PATH -k HG_CONFIG_PATH -t TEXT_PATH -s ljs --speaker_attributes ljs --speaker_text ljs -o results/`


## Inference Voice Conversion demo 
1. Set model paths in `inference_voice_conversion.py`
2. `python inference_voice_conversion.py --vocoder_path HG_PATH
--vocoder_config_path HG_CONFIG_PATH --f0_mean=211.413
--f0_std=46.6595 --energy_mean=0.724884 --energy_std=0.0564605
--output_dir_base=results/ -p data_config.validation_files="{'Dummy': {'basedir': 'data/', 'sampling_rate':'22khz', 'filelist': 'vc_audiopath_txt_speaker_emotion_duration_filelist.txt'}}"`

## LICENSE
Unless otherwise specified, the source code within this repository is provided under the
[MIT License](LICENSE)

## Acknowledgements
The code in this repository is heavily inspired by or makes use of source code from the following works:

- Tacotron implementation from [Keith Ito](https://github.com/keithito/tacotron/)
- STFT code from [Prem Seetharaman](https://github.com/pseeth/pytorch-stft)
- [Masked Autoregressive Flows](https://arxiv.org/abs/1705.07057)
- [Flowtron](https://arxiv.org/abs/2005.05957)
- Source for neural spline functions used in this work: https://github.com/ndeutschmann/zunis 
- Original Source for neural spline functions: https://github.com/bayesiains/nsf 
- Bipartite Architecture based on code from [WaveGlow](https://github.com/NVIDIA/waveglow) 
- [HiFi-GAN](https://github.com/jik876/hifi-gan) 
- [Glow-TTS](https://github.com/jaywalnut310/glow-tts) 

## Relevant Papers

Rohan Badlani, Adrian Łańcucki, Kevin J. Shih, Rafael Valle, Wei Ping, Bryan Catanzaro. <br/>[One TTS Alignment to Rule Them All.](https://ieeexplore.ieee.org/abstract/document/9747707) ICASSP 2022
<br/><br/>
Kevin J Shih, Rafael Valle, Rohan Badlani, Adrian Lancucki, Wei Ping, Bryan Catanzaro. <br/>[RAD-TTS: Parallel flow-based TTS with robust alignment learning and diverse synthesis.](https://openreview.net/pdf?id=0NQwnnwAORi)<br/> ICML Workshop on Invertible Neural Networks, Normalizing Flows, and Explicit Likelihood Models 2021
<br/><br/>
Kevin J Shih, Rafael Valle, Rohan Badlani, Jõao Felipe Santos, Bryan Catanzaro.<br/>[Generative Modeling for Low Dimensional Speech Attributes with Neural Spline Flows.](https://arxiv.org/pdf/2203.01786) Technical Report