@echo off
echo =======================================================
echo Running Selenium Automated Tests for Student Marks App
echo Target: http://localhost:5003
echo =======================================================
py tests\test_marks_calculation.py
pause
