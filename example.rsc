:global ChangeIP do={
    :log info ("ChangeIP")
    :local url "http://10.10.10.50:8080/ipnew"
    :local data "{\"ip\": \"$ip\", \"token\": \"example\"}"
    :local result [/tool fetch url=$url http-method=post http-header-field="Content-Type: application/json" http-data=$data output=user as-value]
    :local response ($result->"data")
    :if ([:find $response "{\"code\": 1}"] = -1) do={
        :put "error"
    }
}
:local newip [/ip address get [find interface=pppoe-out1] address]
:set newip [:pick $newip 0 [:find $newip "/"]]
:local addip [/ip firewall address-list get [find list=public-ip] address]
:if ($newip != $addip) do={
  :log warning ("ipchange: " . $newip)
  /ip firewall address-list set [find list=public-ip] address=$newip
  $ChangeIP ip=$newip
}