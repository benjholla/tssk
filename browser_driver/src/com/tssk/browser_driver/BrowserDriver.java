package com.tssk.browser_driver;

import java.util.logging.Level;
import java.util.logging.Logger;

import net.lightbody.bmp.proxy.ProxyServer;
import net.lightbody.bmp.proxy.http.BrowserMobHttpRequest;
import net.lightbody.bmp.proxy.http.RequestInterceptor;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionGroup;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.PosixParser;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;

public class BrowserDriver {

	private static final String VERSION = "1.0";
	
	// options names
	private static final String HELP_LONG = "help";
	private static final String HELP_SHORT = "h";
	
	private static final String VERSION_LONG = "version";
	private static final String VERSION_SHORT = "v";
	
	private static final String DOMAIN_LONG = "domain";
	private static final String DOMAIN_SHORT = "d";
	
	private static final String URI_LONG = "uri";
	
	private static final String COOKIES_LONG = "cookies";
	private static final String COOKIES_SHORT = "c";
	
	private static final String REFERER_LONG = "referer";
	private static final String REFERER_SHORT = "r";
	
	private static final String USER_AGENT_LONG = "user-agent";
	private static final String USER_AGENT_SHORT = "ua";
	
	private static final String AUTHORIZATION_LONG = "authorization";
	private static final String AUTHORIZATION_SHORT = "auth";
	
	private static final String ACCEPT_LONG = "accept";
	
	private static final String PROXY_PORT_LONG = "proxy-port";
	private static final String PROXY_PORT_SHORT = "p";
	
	// default values
	private static String domain = null;
	private static String uri = null;
	private static String cookies = "";
	private static String referer = "";
	private static String userAgent = "";
	private static String authorization = "";
	private static String accept = "text/plain";
	private static int port = 4444;
	
	public static void main(String[] args) {

		// create the command line parser
		CommandLineParser parser = new PosixParser();

		// create browser driver option groups
		OptionGroup usageOptions = new OptionGroup();
		OptionGroup configurationOptions = new OptionGroup();
		OptionGroup requestOptions = new OptionGroup();
		
		// help option
		Option helpOption = new Option(HELP_SHORT, HELP_LONG, false, "Print usage options.");
		helpOption.setRequired(false);
		usageOptions.addOption(helpOption);
		
		// version option
		Option versionOption = new Option(VERSION_SHORT, VERSION_LONG, false, "Print version.");
		versionOption.setRequired(false);
		usageOptions.addOption(versionOption);
		
		// proxy server port option
		Option proxyOption = new Option(PROXY_PORT_SHORT, PROXY_PORT_LONG, true, "The port to use for the HTTP proxy server.  Default value: 4444.");
		proxyOption.setRequired(false);
		configurationOptions.addOption(proxyOption);
		
		// domain option
		Option domainOption = new Option(DOMAIN_SHORT, DOMAIN_LONG, true, "The domain name of the server (for virtual hosting), and the TCP port number on which the server is listening. The port number may be omitted if the port is the standard port for the service requested.");
		domainOption.setRequired(true);
		requestOptions.addOption(domainOption);
		
		// uri option
		Option uriOption = new Option(URI_LONG, true, "The path for the specified domain.");
		uriOption.setRequired(true);
		requestOptions.addOption(uriOption);
		
		// cookies option
		Option cookiesOption = new Option(COOKIES_SHORT, COOKIES_LONG, true, "An HTTP cookie previously sent by the server with Set-Cookie.  Default value: \"\".");
		cookiesOption.setRequired(false);
		requestOptions.addOption(cookiesOption);
		
		// referer option
		Option refererOption = new Option(REFERER_SHORT, REFERER_LONG, true, "The address of the previous web page from which a link to the currently requested page was followed. Default value: \"\".");
		refererOption.setRequired(false);
		requestOptions.addOption(refererOption);
		
		// user agent option
		Option userAgentOption = new Option(USER_AGENT_SHORT, USER_AGENT_LONG, true, "The user agent string of the user agent.  Default value: \"\".");
		userAgentOption.setRequired(false);
		requestOptions.addOption(userAgentOption);
		
		// authorization option
		Option authorizationOption = new Option(AUTHORIZATION_SHORT, AUTHORIZATION_LONG, true, "Authentication credentials for HTTP authentication.  Default value: \"text/plain\".");
		authorizationOption.setRequired(false);
		requestOptions.addOption(authorizationOption);
		
		// accept option
		Option acceptOption = new Option(ACCEPT_LONG, true, "Content-Types that are acceptable for the response.  Default value: \"text/plain\".");
		acceptOption.setRequired(false);
		requestOptions.addOption(acceptOption);

		Options options = new Options();
		options.addOptionGroup(usageOptions);
		options.addOptionGroup(configurationOptions);
		options.addOptionGroup(requestOptions);
		
		try {
			if(args == null || args.length == 0){
				HelpFormatter formatter = new HelpFormatter();
				formatter.printHelp("ant", options);
				return;
			}
			
			// parse the command line arguments
			CommandLine arguments = parser.parse(options, args);
			
			if (arguments.hasOption(VERSION_LONG)) {
				System.out.println("Browser Driver: " + VERSION);
				return;
			}
			
			if (arguments.hasOption(HELP_LONG)) {
				HelpFormatter formatter = new HelpFormatter();
				formatter.printHelp("ant", options);
				return;
			}
			
			domain = arguments.getOptionValue(DOMAIN_LONG);
			uri = arguments.getOptionValue(URI_LONG);
			
			if (arguments.hasOption(COOKIES_LONG)) {
				cookies = arguments.getOptionValue(COOKIES_LONG);
			}
			
			if (arguments.hasOption(REFERER_LONG)) {
				referer = arguments.getOptionValue(REFERER_LONG);
			}
			
			if (arguments.hasOption(USER_AGENT_LONG)) {
				userAgent = arguments.getOptionValue(USER_AGENT_LONG);
			}
			
			if (arguments.hasOption(AUTHORIZATION_LONG)) {
				authorization = arguments.getOptionValue(AUTHORIZATION_LONG);
			}
			
			if (arguments.hasOption(ACCEPT_LONG)) {
				accept = arguments.getOptionValue(ACCEPT_LONG);
			}
			
			if (arguments.hasOption(PROXY_PORT_LONG)) {
				port = Integer.parseInt(arguments.getOptionValue(PROXY_PORT_LONG));
			}
			
			// load the session into the browser and make the request
			loadSession(domain, uri, cookies, referer, userAgent, authorization, accept, port);
		} catch (Exception e) {
			System.out.println("Unexpected exception:" + e.getMessage());
		}
	}

	public static void loadSession(final String domain, final String uri,
			final String cookies, final String referer, final String userAgent,
			final String authorization, final String accept, final int port) {
		
		// turn off verbose logging
		Logger.getLogger("").setLevel(Level.OFF);

		int result = 0;
		try {
			// start the proxy server
			ProxyServer server = new ProxyServer(port);
			server.start();

			// get the Selenium proxy object
			Proxy proxy = server.seleniumProxy();

			// configure it as a desired capability
			DesiredCapabilities capabilities = new DesiredCapabilities();
			capabilities.setCapability(CapabilityType.PROXY, proxy);

			// start the browser up
			WebDriver driver = new FirefoxDriver(capabilities);

			server.addRequestInterceptor(new RequestInterceptor() {
				@Override
				public void process(BrowserMobHttpRequest request) {
					// rewrite cookies
					request.getMethod().removeHeaders("Cookie");
					request.getMethod().addHeader("Cookie", cookies);

					// rewrite referer
					request.getMethod().removeHeaders("Referer");
					request.getMethod().addHeader("Referer", referer);

					// rewrite user agent
					request.getMethod().removeHeaders("User-Agent");
					request.getMethod().addHeader("User-Agent", userAgent);

					// rewrite authorization
					request.getMethod().removeHeaders("Authorization");
					request.getMethod().addHeader("Authorization",
							authorization);

					// rewrite
					request.getMethod().removeHeaders("Accept");
					request.getMethod().addHeader("Accept", accept);
				}
			});

			// make request
			driver.get("http://" + domain + uri);
		} catch (Exception e) {
			result = -1;
			e.printStackTrace();
		} finally {
			System.exit(result);
		}
	}

}