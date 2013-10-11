# inwx-dyndns: A Python "tool" based on [python-inwx-xmlrpc](http://github.com/pklaus/python-inwx-xmlrpc) for Dynamic DNS

This is a stripped-down version of pklaus' python-inwx-xmlrpc. Nothing is added, there's just a lot removed and one of his examples renamed and slightly adapted (for use of IPv4).


##Usage

1. Log into your inwx.de control panel and add a new A record for a subdomain of your choice.
2. Create a copy of the file `python-inwx-xmlrpc.cfg.example` called `python-inwx-xmlrpc.cfg`, and fill in your credentials, the subdomain and the domain. You can leave everything else as-is.
3. Create a cronjob that calls `python inwx-dyndns.py` every $unit\_of\_time.

##Troubleshooting

If you find this at a much later time than October 2013, the IPv4 lookup service might not exist anymore. Click [here](http://ip.42.pl/raw). Does this show your IP?

If not, replace the value of `IPV4_DETECTION_API` in `inwx-dyndns.py` accordingly.

##Licence

I am forced to license this under the GPLv3. For details, see the file `COPYING`.
