#!/bin/sh
# Filter out YYYYMMDD tagged releases from before
# the switch to semantic versioning as well as
# pYYYYMMDD snapshot tags
git ls-remote --tags https://github.com/xiph/rav1e 2>/dev/null|awk '{ print $2; }' |grep -v '\^{}' |grep 'refs/tags/' |sed -e 's,refs/tags/,,;s,_,.,g' |sed -e 's,^v,,' |grep -vE '^p?2.......$' |sort -V |tail -n1
