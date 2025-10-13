# 常見的PowerShell 輸出訊息的 2 種方法

> **原文發布日期:** 2024-03-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/03/26/powershell-output-to-file
> **標籤:** 無

---

筆記一下輸出到文本的語法

覆蓋該檔 `a.out`

```
$env:path > a.out
```

附加到該檔 `a.out`

```
$env:path >> a.out
```

完整說明

```
 The Windows PowerShell redirection operators use the following characters
  to represent each output type:
    *   All output
    1   Success output
    2   Errors
    3   Warning messages
    4   Verbose output
    5   Debug messages

          NOTE: The All (*), Warning (3), Verbose (4) and Debug (5) redirection operators were introduced
                        in Windows PowerShell 3.0. They do not work in earlier versions of Windows PowerShell.

  The Windows PowerShell redirection operators are as follows.
  Operator  Description                Example
  --------  ----------------------     ------------------------------
  >         Sends output to the        Get-Process > Process.txt
            specified file.

  >>        Appends the output to      dir *.ps1 >> Scripts.txt
            the contents of the
            specified file.

  2>        Sends errors to the        Get-Process none 2> Errors.txt
            specified file.

  2>>       Appends errors to          Get-Process none 2>> Save-Errors.txt
            the contents of the
            specified file.

  2>&1      Sends errors (2) and       Get-Process none, Powershell 2>&1
            success output (1)
            to the success
            output stream.

  3>        Sends warnings to the      Write-Warning "Test!" 3> Warnings.txt
            specified file.

  3>>       Appends warnings to        Write-Warning "Test!" 3>> Save-Warnings.txt
            the contents of the
            specified file.

  3>&1      Sends warnings (3) and     function Test-Warning
            success output (1)         {  Get-Process PowerShell;
            to the success                Write-Warning "Test!" }
            output stream.             Test-Warning 3>&1

  4>        Sends verbose output to    Import-Module * -Verbose 4> Verbose.txt
            the specified file.

  4>>       Appends verbose output     Import-Module * -Verbose 4>> Save-Verbose.txt
            to the contents of the
            specified file.

  4>&1      Sends verbose output (4)   Import-Module * -Verbose 4>&1
            and success output (1)
            to the success output
            stream.

  5>        Sends debug messages to    Write-Debug "Starting" 5> Debug.txt
            the specified file.

  5>>       Appends debug messages     Write-Debug "Saving" 5>> Save-Debug.txt
            to the contents of the
            specified file.

  5>&1      Sends debug messages (5)   function Test-Debug
            and success output (1)     { Get-Process PowerShell
            to the success output        Write-Debug "PS" }
            stream.                    Test-Debug 5>&1

  *>        Sends all output types     function Test-Output
            to the specified file.     { Get-Process PowerShell, none
                                         Write-Warning "Test!"
  *>>       Appends all output types     Write-Verbose "Test Verbose"
            to the contents of the       Write-Debug "Test Debug" }
            specified file.
                                       Test-Output *> Test-Output.txt
  *>&1      Sends all output types     Test-Output *>> Test-Output.txt
            (*) to the success output  Test-Output *>&1
            stream.

The syntax of the redirection operators is as follows:

   <input> <operator> [<path>\]<file>

If the specified file already exists, the redirection operators that do not
append data (> and n>) overwrite the current contents of the file without
warning. However, if the file is a read-only, hidden, or system file, the
redirection fails. The append redirection operators (>> and n>>) do not
write to a read-only file, but they append content to a system or hidden
file.

To force the redirection of content to a read-only, hidden, or system file,
use the Out-File cmdlet with its Force parameter. When you are writing to
files, the redirection operators use Unicode encoding. If the file has a
different encoding, the output might not be formatted correctly. To
redirect content to non-Unicode files, use the Out-File cmdlet with its
Encoding parameter.
```

## REF

[What does '>>' do in powershell? - Stack Overflow](https://stackoverflow.com/questions/35088340/what-does-do-in-powershell)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [PowerShell](/jakeuj/Tags?qq=PowerShell)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
