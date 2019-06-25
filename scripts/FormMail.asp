<%@ LANGUAGE="VBScript" %>
<% '***************************************************************************
   '* ASP FormMail                                                            *
   '*                                                                         *
   '* Do not remove this notice.                                              *
   '*                                                                         *
   '* Copyright 1999-2002 by Mike Hall.                                       *
   '* Please see http://www.brainjar.com for documentation and terms of use.  *
   '***************************************************************************

   '- Customization of these values is required, see documentation. -----------

   referers   = Array("north-muskoka.com")
   recipientDomains = Array("north-muskoka.com")
   mailComp   = "CDOSYS"
   smtpServer = "127.0.0.1"
   fromAddr   = "webmaster@north-muskoka.com"

   '- End required customization section. -------------------------------------

   Response.Buffer = true
   errorMsgs = Array()

   'Check for form data.

   if Request.ServerVariables("Content_Length") = 0 then
     call AddErrorMsg("No form data submitted.")
   end if

   'Check if referer is allowed.

   if UBound(referers) >= 0 then
     validReferer = false
     referer = GetHost(Request.ServerVariables("HTTP_REFERER"))
     for each host in referers
       if host = referer or right(referer, len(host)+1) = "." & host then
         validReferer = true
       end if
     next
     if not validReferer then
       if referer = "" then
         call AddErrorMsg("No referer.")
       else
         call AddErrorMsg("Invalid referer: '" & referer & "'.")
       end if
     end if
   end if

   'Check for the recipients field.

   if Request.Form("_recipients") = "" then
     call AddErrorMsg("Missing email recipient.")
   end if

   'Check all recipient email addresses.

   recipients = Split(Request.Form("_recipients"), ",")
   for each name in recipients
     name = Trim(name)
     if not IsValidEmailAddress(name) then
       call AddErrorMsg("Invalid or disallowed email address in recipient list: " & name & ".")
     end if
   next
   recipients = Join(recipients, ",")

   'Get replyTo email address from specified field, if given, and check it.

   name = Trim(Request.Form("_replyToField"))
   if name <> "" then
     replyTo = Request.Form(name)
   else
     replyTo = Request.Form("_replyTo")
   end if
   if replyTo <> "" then
     if not IsValidEmailAddress(replyTo) then
       call AddErrorMsg("Invalid email address in reply-to field: " & replyTo & ".")
     end if
   end if

   'Get subject text.

   subject = Request.Form("_subject")

   'If required fields are specified, check for them.

   if Request.Form("_requiredFields") <> "" then
     required = Split(Request.Form("_requiredFields"), ",")
     for each name in required
       name = Trim(name)
       if Left(name, 1) <> "_" and Request.Form(name) = "" then
         call AddErrorMsg("Missing value for " & name)
       end if
     next
   end if

   'If a field order was given, use it. Otherwise use the order the fields were
   'received in.

   str = ""
   if Request.Form("_fieldOrder") <> "" then
     fieldOrder = Split(Request.Form("_fieldOrder"), ",")
     for each name in fieldOrder
       if str <> "" then
         str = str & ","
       end if
       str = str & Trim(name)
     next
     fieldOrder = Split(str, ",")
   else
     fieldOrder = FormFieldList()
   end if

   'If there were no errors, build the email note and send it.

   if UBound(errorMsgs) < 0 then

     'Build table of form fields and values.

     body = "<table border=""0"" cellpadding=""2"" cellspacing=""0"">" & vbCrLf
     for each name in fieldOrder
       body = body _
            & "<tr valign=""top"">" _
            & "<td><b>" & name & ":</b></td>" _
            & "<td>" & Request.Form(name) & "</td>" _
            & "</tr>" & vbCrLf
     next
     body = body & "</table>" & vbCrLf

     'Add a table for any requested environmental variables.

     if Request.Form("_envars") <> "" then
       body = body _
            & "<p>&nbsp;</p>" & vbCrLf _
            & "<table border=""0"" cellpadding=""2"" cellspacing=""0"">" & vbCrLf
       envars = Split(Request.Form("_envars"), ",")
       for each name in envars
         name = Trim(name)
         body = body _
              & "<tr valign=""top"">" _
              & "<td><b>" & name & ":</b></td>" _
              & "<td>" & Request.ServerVariables(name) & "</td>" _
              & "</tr>" & vbCrLf
       next
       body = body & "</table>" & vbCrLf
     end if

     'Send it.

     str = SendMail()
     if str <> "" then
       AddErrorMsg(str)
     end if

     'Redirect if a URL was given.

     if Request.Form("_redirect") <> "" then
       Response.Redirect(Request.Form("_redirect"))
     end if

   end if %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<title>Form Mail</title>
<style type="text/css">

body {
  background-color: #ffffff;
  color: #000000;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10pt;
}

table {
  border: solid 1px #000000;
  border-collapse: collapse;
}

td, th {
  border: solid 1px #000000;
  border-collapse: collapse;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10pt;
  padding: 2px;
  padding-left: 8px;
  padding-right: 8px;
}

th {
  background-color: #c0c0c0;
}

.error {
  color: #c00000;
}

</style>
</head>
<body>

<% if UBound(errorMsgs) >= 0 then %>
<p class="error">Form could not be processed due to the following errors:</p>
<ul>
<%   for each msg in errorMsgs %>
  <li class="error"><% = msg %></li>
<%   next %>
</ul>
<% else %>
<table cellpadding="0" cellspacing="0">
<tr>
  <th colspan="2" valign="bottom">
  Thank you, the following information has been sent:
  </th>
</tr>
<%   for each name in fieldOrder %>
<tr valign="top">
  <td><b><% = name %></b></td>
  <td><% = Request.Form(name) %></td>
</tr>
<%   next %>
</table>
<% end if %>

</body>
</html>

<% '---------------------------------------------------------------------------
   ' Subroutines and functions.
   '---------------------------------------------------------------------------

   sub AddErrorMsg(msg)

     dim n

    'Add an error message to the list.

     n = UBound(errorMsgs)
     Redim Preserve errorMsgs(n + 1)
     errorMsgs(n + 1) = msg

   end sub

   function GetHost(url)

     dim i, s

     GetHost = ""

     'Strip down to host or IP address and port number, if any.

     if Left(url, 7) = "http://" then
       s = Mid(url, 8)
     elseif Left(url, 8) = "https://" then
       s = Mid(url, 9)
     end if
     i = InStr(s, "/")
     if i > 1 then
       s = Mid(s, 1, i - 1)
     end if

     getHost = s

   end function

   'Define the global list of valid TLDs.

   dim validTlds

   function IsAllowedRecipientDomain(domain)

   'Check if domain is in recipientDomains array.

	 for each host in recipientDomains
		 if host = domain then
		   IsAllowedRecipientDomain = true
		   exit function
		 end if
	 next

	 IsAllowedRecipientDomain = false

	 end function

   function IsValidEmailAddress(emailAddr)

     dim i, localPart, domain, charCode, subdomain, subdomains, tld

     'Check for valid syntax in an email address.

     IsValidEmailAddress = true

     'Parse out the local part and the domain.

     i = InStrRev(emailAddr, "@")
     if i <= 1 then
       IsValidEmailAddress = false
       exit function
     end if
     localPart = Left(emailAddr, i - 1)
     domain = Mid(emailAddr, i + 1)
     if Len(localPart) < 1 or Len(domain) < 3 then
       IsValidEmailAddress = false
       exit function
     end if

     'Check for invalid characters in the local part.

     for i = 1 to Len(localPart)
       charCode = Asc(Mid(localPart, i, 1))
       if charCode < 32 or charCode >= 127 then
         IsValidEmailAddress = false
         exit function
       end if
     next

     'Check for invalid characters in the domain.

     domain = LCase(domain)
     for i = 1 to Len(domain)
       charCode = Asc(Mid(domain, i, 1))
       if not ((charCode >= 97 and charCode <= 122) or (charCode >= 48 and charCode <= 57) or charCode = 45 or charCode = 46) then
         IsValidEmailAddress = false
         exit function
       end if
     next

     'Check if domain part is in recipientDomains array.'
     if not IsAllowedRecipientDomain(domain) then
       IsValidEmailAddress = false
       exit function
     end if

     'Check each subdomain.

     subdomains = Split(domain, ".")
     for each subdomain in subdomains
       if Len(subdomain) < 1 then
         IsValidEmailAddress = false
         exit function
       end if
     next

     'Last subdomain should be a TLD.

     tld = subdomains(UBound(subdomains))
     if not IsArray(validTlds) then
       call SetValidTlds()
     end if
     for i = LBound(validTlds) to UBound(validTlds)
       if tld = validTlds(i) then
         exit function
       end if
     next
     IsValidEmailAddress = false

   end function

   sub setValidTlds()

     'Load the global list of valid TLDs.

     validTlds = Array("aero", "biz", "com", "coop", "edu", "gov", "info", "int", "mil", "museum", "name", "net", "org", "pro", _
       "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", "as", "at", "au", "aw", "az", _
       "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", _
       "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "cr", "cu", "cv", "cx", "cy", "cz", _
       "de", "dj", "dk", "dm", "do", "dz", "ec", "ee", "eg", "eh", "er", "es", "et", _
       "fi", "fj", "fk", "fm", "fo", "fr", _
       "ga", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy", _
       "hk", "hm", "hn", "hr", "ht", "hu", _
       "id", "ie", "il", "im", "in", "io", "iq", "ir", "is", "it", _
       "je", "jm", "jo", "jp", _
       "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", _
       "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "lu", "lv", "ly", _
       "ma", "mc", "md", "mg", "mh", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw ", "mx", "my", "mz", _
       "na", "nc", "ne", "nf", "ng", "ni", "nl", "no", "np", "nr", "nu", "nz", _
       "om", _
       "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "ps", "pt", "pw", "py", _
       "qa", _
       "re", "ro", "ru", "rw", _
       "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", "so", "sr", "st", "sv", "sy", "sz", _
       "tc", "td", "tf", "tg", "th", "tj", "tk", "tm", "tn", "to", "tp", "tr", "tt", "tv", "tw", "tz", _
       "ua", "ug", "uk", "um", "us", "uy", "uz", _
       "va", "vc", "ve", "vg", "vi", "vn", "vu", _
       "wf", "ws", _
       "ye", "yt", "yu", _
       "za", "zm", "zw")

   end sub

   function FormFieldList()

     dim str, i, name

     'Build an array of form field names ordered as they were received.

     str = ""
     for i = 1 to Request.Form.Count
       for each name in Request.Form
         if Left(name, 1) <> "_" and Request.Form(name) is Request.Form(i) then
           if str <> "" then
             str = str & ","
           end if
           str = str & name
           exit for
         end if
       next
     next
     FormFieldList = Split(str, ",")

   end function

   function SendMail()

     dim mailObj, cdoMessage, cdoConfig
     dim addrList

     'Send email based on mail component. Uses global variables for parameters
     'because there are so many.

     SendMail = ""

     'Send email (CDOSYS version).

     if mailComp = "CDOSYS" then
       set cdoMessage = Server.CreateObject("CDO.Message")
       set cdoConfig = Server.CreateObject("CDO.Configuration")
       cdoConfig.Fields("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
       cdoConfig.Fields("http://schemas.microsoft.com/cdo/configuration/smtpserver") = smtpServer
       cdoConfig.Fields.Update
       set cdoMessage.Configuration = cdoConfig
			 cdoMessage.Fields.Item("urn:schemas:mailheader:X-HTTP-Host") = Request.ServerVariables("HTTP_HOST")
			 cdoMessage.Fields.Update
       cdoMessage.From =  fromAddr
       cdoMessage.ReplyTo = replyTo
       cdoMessage.To = recipients
       cdoMessage.Subject = subject
       cdoMessage.HtmlBody = body
       on error resume next
       cdoMessage.Send
       if Err.Number <> 0 then
         SendMail = "Email send failed: " & Err.Description & "."
       end if
       set cdoMessage = Nothing
       set cdoConfig = Nothing
       exit function
     end if

     'Send email (JMail version).

     if mailComp = "JMail" then
       set mailObj = Server.CreateObject("JMail.SMTPMail")
			 mailObj.ISOEncodeHeaders = False
			 mailObj.AddHeader "HTTP-Host", Request.ServerVariables("HTTP_HOST")
       mailObj.Silent = true
       mailObj.ServerAddress = smtpServer
       mailObj.Sender = fromAddr
       mailObj.ReplyTo = replyTo
       mailObj.Subject = subject
       addrList = Split(recipients, ",")
       for each addr in addrList
         mailObj.AddRecipient Trim(addr)
       next
       mailObj.ContentType = "text/html"
       mailObj.Body = body
       if not mailObj.Execute then
         SendMail = "Email send failed: " & mailObj.ErrorMessage & "."
       end if
       exit function
     end if

   end function %>
