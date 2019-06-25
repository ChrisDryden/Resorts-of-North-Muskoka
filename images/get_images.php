<?php
	//get all image files in gallery folder and output as html <img> tags

	$dir = new DirectoryIterator("images/photogallery/");
	foreach ($dir as $fileinfo) {
		$filename = $fileinfo->getFilename();
		$ext_array = explode('.',$filename);
		$ext = strtolower($ext_array[1]);

		if ($ext == "jpg" || $ext == "jpeg" || $ext == "png") {
			echo "<img src='images/photogallery/$filename'>\n";
		}
	}