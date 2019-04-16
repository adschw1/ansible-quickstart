"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class BuildTopology( Topo ):


    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        R1 = self.addHost( 'R1' )
        R2 = self.addHost( 'R2' )
        R3 = self.addHost( 'R3' )

        S1 = self.addSwitch( 'S1' )
        S2 = self.addSwitch( 'S2' )
        S3 = self.addSwitch( 'S3' )

        PC1 = self.addHost('PC1')
	PC2 = self.addHost('PC2')
        PC3 = self.addHost('PC3')
	PC4 = self.addHost('PC4')
	PC5 = self.addHost('PC5')
        PC6 = self.addHost('PC6')
        PC7 = self.addHost('PC7')
        PC8 = self.addHost('PC8')
        PC9 = self.addHost('PC9')
        PC10 = self.addHost('PC10')

        # Add links
        self.addLink( S1, R1 )
  


topos = { 'mytopo': ( lambda: BuildTopology() ) }

