package com.example.androidocr.camera

import android.annotation.SuppressLint
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import com.google.mlkit.vision.common.InputImage

private class YourImageAnalyzer : ImageAnalysis.Analyzer {

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    @SuppressLint("UnsafeOptInUsageError")
    override fun analyze(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image
        if (mediaImage != null) {
            val image = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)
            // Pass image to an ML Kit Vision API
        }
    }
}