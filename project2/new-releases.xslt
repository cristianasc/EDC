<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:html="http://www.w3.org/1999/xhtml"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:foaf="http://xmlns.com/foaf/0.1/">

  <xsl:template match="albums">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.new-releases.com/">
        <xsl:apply-templates/>
      </rdf:Description>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="items">
    <xsl:variable name="href"><xsl:value-of select="href"/></xsl:variable>
      <rdf:Description rdf:about="{$href}">
        <foaf:album_type><xsl:value-of select="album_type"/></foaf:album_type>
        <foaf:external_urls><xsl:value-of select="external_urls/spotify"/></foaf:external_urls>
        <foaf:id><xsl:value-of select="id"/></foaf:id>
        <foaf:href><xsl:value-of select="href"/></foaf:href>
        <foaf:href><xsl:value-of select="available_markets"/></foaf:href>
      </rdf:Description>
  </xsl:template>

  <xsl:template match="items/artists">
      <xsl:variable name="artists_id"><xsl:value-of select="id"/></xsl:variable>
        <rdf:Description rdf:about="http://www.new-releases.com/artists/{$artists_id}">
            <foaf:external_urls_spotify>
                <xsl:value-of select="external_urls/spotify"/>
            </foaf:external_urls_spotify>
            <foaf:href>
                <xsl:value-of select="href"/>
            </foaf:href>
            <foaf:id>
                <xsl:value-of select="id"/>
            </foaf:id>
            <foaf:name>
                <xsl:value-of select="name"/>
            </foaf:name>
            <foaf:type>
                <xsl:value-of select="type"/>
            </foaf:type>
            <foaf:uri>
                <xsl:value-of select="uri"/>
            </foaf:uri>
        </rdf:Description>
    </xsl:template>

    <xsl:template match="items/images">
      <xsl:variable name="url"><xsl:value-of select="url"/></xsl:variable>
        <rdf:Description rdf:about="{$url}">
            <foaf:height>
                <xsl:value-of select="height"/>
            </foaf:height>
            <foaf:width>
                <xsl:value-of select="width"/>
            </foaf:width>
        </rdf:Description>
    </xsl:template>
</xsl:stylesheet>