Summary:	AIM transport for Jabber
Name:		pyaim-t
Version:	0.6
Release:	1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://www.blathersource.org/download.php/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	cf20fd8593a8463426e720c2faf7d629
Source2:	pyaim-t.init
Source3:	pyaim-t.sysconfig
Source4:	pyaim-t.xml
URL:		http://pyaim-t.blathersource.org/
PreReq:		rc-scripts
Requires:	python-TwistedWeb
Requires:	python-TwistedWords
Requires:	python-TwistedXish
Requires(post):	jabber-common
Requires(post):	perl-base
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with AIM servers.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami AIM.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd14,%{_sysconfdir}/jabber} \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install src/aimtrans.so $RPM_BUILD_ROOT%{_libdir}/jabberd14
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-aimtrans
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-aimtrans
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/aimtrans.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in the config file..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/pyaim-t.xml
	fi
fi

/sbin/chkconfig --add jabber-aimtrans
if [ -r /var/lock/subsys/jabber-aimtrans ]; then
	/etc/rc.d/init.d/jabber-aimtrans restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-aimtrans start\" to start Jabber aim transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/pyaim-t ]; then
		/etc/rc.d/init.d/pyaim-t stop >&2
	fi
	/sbin/chkconfig --del pyaim-t
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README INSTALL
%attr(755,root,root) %{_sbindir}/PyAIMt
%{_libdir}/%{name}
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
