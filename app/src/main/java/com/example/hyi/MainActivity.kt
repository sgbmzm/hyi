package com.example.hyi

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {

    lateinit var spinnerYear: Spinner
    lateinit var buttonCalculate: Button
    lateinit var textViewResult: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        spinnerYear = findViewById(R.id.spinnerYear)
        buttonCalculate = findViewById(R.id.buttonCalculate)
        textViewResult = findViewById(R.id.textViewResult)

        // אתחול Python
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        val py = Python.getInstance()
        val hyi = py.getModule("hyi") // שם הקובץ Python שלך בלי .py

        // דוגמה: Spinner עם שנים
        val years = (5700..5800).toList() // טווח שנים לדוגמה
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, years)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerYear.adapter = adapter

        buttonCalculate.setOnClickListener {
            try {
                val selectedYear = spinnerYear.selectedItem as Int
                val result: PyObject = hyi.callAttr("main_result", selectedYear)

                // המרה לרשימה ב-Kotlin
                val resultList = result.asList()

                // שימוש ב-StringBuilder להוספת ירידת שורה בין כל איבר
                val sb = StringBuilder()
                for (item in resultList) {
                    sb.append(item.toString().replace("\n", "")).append("\n\n")
                }

                textViewResult.text = sb.toString()
            } catch (e: Exception) {
                textViewResult.text = "שגיאה: ${e.message}"
            }
        }
    }
}


