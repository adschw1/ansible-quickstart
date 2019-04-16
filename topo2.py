"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        middleHost = self.addHost( 'h1' )
        leftHost = self.addHost( 'h2' )
        rightTopHost = self.addHost( 'h3' )
        rightBottomHost = self.addHost( 'h4' )
        rightSwitch = self.addSwitch( 's1' )
        middleSwitch = self.addSwitch( 's2' )
        leftSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, middleSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( middleSwitch, rightSwitch )
        self.addLink( middleSwitch, middleHost )
        self.addLink( rightSwitch, rightTopHost )
        self.addLink( rightSwitch, rightBottomHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
