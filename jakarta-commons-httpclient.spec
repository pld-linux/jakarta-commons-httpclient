%define	short_name	httpclient
Summary:	Jakarta Commons HTTPClient Package
Summary(pl.UTF-8):   Pakiet Jakarta Commons HTTPClient
Name:		jakarta-commons-%{short_name}
Version:	2.0.2
Release:	0.1
License:	Apache Software License
Source0:	http://archive.apache.org/dist/jakarta/commons/httpclient/source/commons-httpclient-%{version}-src.tar.gz
Group:		Development/Languages/Java
URL:		http://jakarta.apache.org/commons/httpclient/
BuildRequires:	ant
BuildRequires:	jakarta-commons-logging >= 1.0.3
BuildRequires:	jce >= 1.2.2
BuildRequires:	jsse >= 1.0.3.01
BuildRequires:	junit
Requires:	jakarta-commons-logging >= 1.0.3
Provides:	commons-%{short_name}
Obsoletes:	commons-%{short_name}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most
significant protocol used on the Internet today. Web services,
network-enabled appliances and the growth of network computing
continue to expand the role of the HTTP protocol beyond user-driven
web browsers, and increase the number of applications that may require
HTTP support. Although the java.net package provides basic support for
accessing resources via HTTP, it doesn't provide the full flexibility
or functionality needed by many applications. The Jakarta Commons HTTP
Client component seeks to fill this void by providing an efficient,
up-to-date, and feature-rich package implementing the client side of
the most recent HTTP standards and recommendations. Designed for
extension while providing robust support for the base HTTP protocol,
the HTTP Client component may be of interest to anyone building
HTTP-aware client applications such as web browsers, web service
clients, or systems that leverage or extend the HTTP protocol for
distributed communication.

%description -l pl.UTF-8
Protokół przesyłania hypertekstu (HTTP - Hyper-Text Transfer Protocol)
jest prawdopodobnie najbardziej znaczącym z używanych obecnie
protokołów w Internecie. Usługi WWW, zastosowania sieciowe i rozwój
usług sieciowych nadal rozszerza rolę protokołu HTTP poza przeglądarki
obsługiwane przez użytkownika i zwiększa liczbę aplikacji mogących
potrzebować obsługi HTTP. Mimo że pakiet java.net udostępnia
podstawową obsługę dostępu do zasobów poprzez HTTP, nie dostarcza
pełnej elastyczności czy funkcjonalności potrzebnej wielu aplikacjom.
Komponent Jakarta Commons HTTP Client stara się wypełnić tę lukę
dostarczając wydajny, aktualny i bogaty w możliwości pakiet
implementujący kliencką stronę najnowszych standardów i rekomendacji
HTTP. Zaprojektowany do rozszerzania, a jednocześnie dostarczający
bogatą obsługę podstawowego protokołu HTTP, komponent HTTP Client może
być interesujący dla każdego tworzącego aplikacje klienckie
obsługujące HTTP, takie jak przeglądarki WWW, klientów usług WWW czy
systemy wykorzystujące lub rozszerzające protokół HTTP do komunikacji
rozproszonej.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):   Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package demo
Summary:	Demos for %{name}
Summary(pl.UTF-8):   Programy demonstracyjne dla pakietu %{name}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demos for %{name}.

%description demo -l pl.UTF-8
Programy demonstracyjne dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl.UTF-8):   Podręcznik dla pakietu %{name}
Group:		Documentation

%description manual
Manual for %{name}.

%description manual -l pl.UTF-8
Podręcznik dla pakietu %{name}.

%prep
%setup -q -n commons-httpclient-%{version}
mkdir lib # duh
rm -rf docs/apidocs docs/*.patch docs/*.orig docs/*.rej

%build
export CLASSPATH=%(build-classpath jsse jce junit jakarta-commons-logging)
ant \
	-Dbuild.sysclasspath=first \
	-Djavadoc.j2sdk.link=%{_javadocdir}/java \
	-Djavadoc.logging.link=%{_javadocdir}/jakarta-commons-logging \
	dist test-nohost

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/commons-%{short_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`
done
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}
mv dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# demo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr src/examples src/contrib $RPM_BUILD_ROOT%{_datadir}/%{name}

# manual and docs
mv dist/docs/USING_HTTPS.txt .
rm -f dist/docs/{BUILDING,TESTING}.txt
ln -s %{_javadocdir}/%{name} dist/docs/apidocs

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt RELEASE_NOTES.txt USING_HTTPS.txt
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}

%files manual
%defattr(644,root,root,755)
%doc dist/docs/*
