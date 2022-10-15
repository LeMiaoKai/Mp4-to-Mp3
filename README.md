# How to extract mp3 from mp4 file
## Even the mp4 file only incloud the audio clip, for example, the audios download from youtube without video clip.
 
关于如何将Mp4转换为Mp3的文章很多，方案也都很有效。但是这其中的大部分方法，并不适用于该Mp4文件中仅包含音频内容的情况，比如：有人从YouTube，下载了仅包含音频内容的文件，这个文件其实还是Mp4格式的，只是没有视频内容，虽然可以通过直接将后缀名改为.mp3，将这个本质是Mp4的文件变为一个伪Mp3文件，也可以在一些播放器上进行播放，但终究不是真正的音频文件，我试过把这个文件放到foobar2000中播放，但是会被识别为无效的内容，而不能播放，如果将后缀改为mp4后，就可以正常的播放声音了。

那要如何把这个Mp4文件变成真正的mp3文件呢？

方法很简单，先要在Python中安装moviepy模块，可以通过 pip install moviepy 进行加载，之后就是几行代码可以解决的事情了，详见代码及注释。

这份代码是我用TKinter编译的一个用于转换Mp4的简易程序，界面如下：
![image](https://user-images.githubusercontent.com/106961670/195970084-c40fe4fa-aa5f-46da-a743-17bf5271ef86.png)
以上内容，希望能对你有所启发，如有不足之处，请指出，谢谢！
