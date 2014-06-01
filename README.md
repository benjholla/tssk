Tactical Session Stealing Kit
===============================
(or tssk tssk why are you not using https?!)

# Overview
TODO: More details coming soon...

## Session Stealing

`python tssk.py -h`

    Usage: tssk [options] ...
    Configuration:
      --tshark <filepath>      Sets the path to tshark.
    Processing:
      --pcap <filepath>        Sets the path to the pcap file to parse.
      --device <id or name>    Sets the device on which to capture traffic.
    Miscellaneous:
      -h                       Print usage options.
      -v                       Print version.
      -d                       Enable debug messages (verbose mode).

## Browser Driver

The Browser Driver is a no frills combination of a Selenium web driver and the Browsermob Proxy for sending and rewriting HTTP requests.  The driver Jar can be used on the command line or included in a project.

`java -jar driver.jar -h`

    usage: driver [options] ...
     -acc,--accept <arg>           Content-Types that are acceptable for the response.  Default value: "text/plain".
     -auth,--authorization <arg>   Authentication credentials for HTTP authentication.  Default value: "".
     -c,--cookies <arg>            An HTTP cookie previously sent by the server with Set-Cookie.  Default value: "".
     -d,--domain <arg>             The domain name of the server (for virtual hosting), and the TCP port number on which
                                   the server is listening. The port number may be omitted if the port is the standard
                                   port for the service requested.
     -h,--help                     Print usage options.
     -p,--proxy-port <arg>         The port to use for the HTTP proxy server.  Default value: 4444.
     -r,--referer <arg>            The address of the previous web page from which a link to the currently requested
                                   page was followed. Default value: "".
     -u,--uri <arg>                The path for the specified domain.
     -ua,--user-agent <arg>        The user agent string of the user agent.  Default value: "".
     -v,--version                  Print version.
