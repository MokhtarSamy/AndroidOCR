package com.example.androidocr.camera

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import com.google.mlkit.vision.label.ImageLabel

class LabelsImage( private val label: ImageLabel) {

    private val rectPaint = Paint().apply {
        color = Color.WHITE
        style = Paint.Style.STROKE
        strokeWidth = 4.0f
    }
    private val textPaint = Paint().apply {
        color = Color.WHITE
        textSize = 36.0f
    }
}